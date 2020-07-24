# logica voor aggregeren van data
# TODO Deze logica moet verplaatst worden naar een externe API

import logging
from applicatie.logic.controles import geef_codechecklijst

_logger = logging.getLogger(__file__)

# Definieer keys gebruikt in algoritme
GETELD_KEY = '_geteld'
NUMGETELD_KEY = '_numgeteld'
IS_TUSSENTOTAAL = '_is_tussentotaal'

# TODO Misschien ook de volgende attributen aan elk record toevoegen ivm nog te bouwen mutatiefunctionaliteit:
# _parent_rijcode
# _parent_kolomcode


def aggregeren_volledig(data, defbestand):
    """"Volledige dataset aggregeren.


    Per rekening specificeren we de dimensies
    waarover geaggregeerd moet worden.
    """
    data_geaggregeerd = dict()
    fouten_aggregeren = list()

    cl = defbestand['codelijsten']
    codechecklijst = geef_codechecklijst(cl)

    # 1: rekening 'lasten' aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['lasten'],
        ['categorie', 2, 'categorie_lasten'],
        ['taakveld', 2, 'taakveld'],
        codechecklijst
    )
    data_geaggregeerd['lasten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # 2: rekening 'balans_lasten' aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['balans_lasten'],
        ['categorie', 2, 'categorie_lasten'],
        ['balanscode', 2, 'balanscode'],
        codechecklijst
    )
    data_geaggregeerd['balans_lasten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # 3: rekening 'baten' aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['baten'],
        ['categorie', 2, 'categorie_baten'],
        ['taakveld', 2, 'taakveld'],
        codechecklijst
    )
    data_geaggregeerd['baten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # 4: rekening 'balans_baten' aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['balans_baten'],
        ['categorie', 2, 'categorie_baten'],
        ['balanscode', 2, 'balanscode'],
        codechecklijst
    )
    data_geaggregeerd['balans_baten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # 5: rekening 'balans_standen' aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['balans_standen'],
        ['standper', -1, 'standper'],  # aggregatieniveau -1 betekent niet aggregeren
        ['balanscode', 2, 'balanscode'],
        codechecklijst
    )
    data_geaggregeerd['balans_standen'] = data_agg
    fouten_aggregeren.extend(fouten)

    return data_geaggregeerd, fouten_aggregeren


def aggregeren_rekening(data, dimensie_1, dimensie_2, codechecklijst):
    """Data voor een rekening volledig aggregeren over twee dimensies

    We specificeren hiervoor dimensie_1 en dimensie_2, dit zijn lists:
    [ naam dimensie, aggregatieniveau, naam codelijst ]
    """
    foutenlijst = list()

    # aggregeren over dimensie 1
    vastedims = [dimensie_2[0], 'sub_'+dimensie_2[0], 'bedrag']   # we houden de tweede dimensie vast
    aggdim, aggniv, clnaam = dimensie_1
    clijst = codechecklijst.get(clnaam)
    if aggniv > -1:
        data, fouten = aggregeren_data(data, aggdim, vastedims, aggniv, clijst, False)
        foutenlijst.extend(fouten)

    # aggregeren over dimensie 2
    vastedims = [dimensie_1[0], 'sub_'+dimensie_1[0], 'bedrag']   # we houden de eerste dimensie vast
    aggdim, aggniv, clnaam = dimensie_2
    clijst = codechecklijst.get(clnaam)
    data, fouten = aggregeren_data(data, aggdim, vastedims, aggniv, clijst, True)
    foutenlijst.extend(fouten)

    # TODO Ik wil eigenlijk juist kunnen achterhalen of iets geteld is of niet
    data = data_opschonen(data, [GETELD_KEY, NUMGETELD_KEY])

    # toevoegen van omschrijving aan de gekozen dimensie
    aggdim, aggniv, clnaam = dimensie_2
    clijst = codechecklijst.get(clnaam)

    # TODO Moet het toevoegen van een omschrijving hier gebeuren?
    # Omschrijving staat nu in tabel via een andere oplossing
    # Weggehaald omdat deze omschrijving ook in de download terechtkwam
    # data = data_toevoegen_omschrijving(data, aggdim, clijst)

    return data, foutenlijst


def data_opschonen(data, keylist):
    # data is een list van records (dicts)
    # verwijder de opgegeven keys uit alle records

    data_schoon = [{k: v for (k, v) in record.items() if k not in keylist}
                   for record in data]

    return data_schoon


def data_toevoegen_omschrijving(data, dimensie, clijst):
    """"Toevoegen van een omschrijving aan codes"""

    cds = clijst[0::4]  # cds: lijst van codes
    oms = clijst[1::4]  # oms: omschrjving van codes

    for rec in data:
        k2 = ''
        v2 = ''
        for k, v in rec.items():
            if k == dimensie:
                omschrijving = oms[cds.index(v)] if v in cds else ''
                k2 = k + ':'
                v2 = v if omschrijving == '' else v + ' ' + omschrijving
        if not k2 == '':
            rec.update({k2: v2})

    return data


def aggregeren_data(data, dimensie, vastedims, aggniveau, clijst, alleen_geteld):
    """aggregeren data: lijst van data records (dicts)."""
    # Laatste wijziging 6 april 2019 (getest in Jupyter notebook)

    agg_data = list()
    fouten = list()

    if not clijst:
        fouten.append("Geen codelijst beschikbaar voor {}.".format(dimensie))
        return agg_data, fouten

    if aggniveau < 0:
        # stoppen indien aggregatieniveau negatief
        # TODO: Maar -1 betekende toch niet aggregeren??
        fouten.append("Aggregatieniveau mag niet negatief zijn.")
        return agg_data, fouten

    cds = clijst[0::4]  # cds: lijst van codes
    niv = clijst[2::4]  # niv: niveau van codes in de codelijst (0 = hoogste niveau)
    ptc = clijst[3::4]  # ptc: lijst van parent codes behorende bij de codes

    def aggregeren_record(recs, errs, record, dimensie, vastedims, aggniveau, cds, niv, ptc):
        """Recursieve functie om een record uit data 
        te aggregeren tot op het laagste niveau"""""

        def tel_record(record, dimensie, vastedimensies, aggniv, cds, niv, ptc):
            geteld_record = dict()
            telfouten = list()
            if aggniv == 0:
                # niveau waarop we stoppen met doortellen
                return geteld_record, telfouten
            if GETELD_KEY in record:
                # stoppen indien record eerder als 'niet geteld' is gemarkeerd
                if record.get(GETELD_KEY) is False:
                    return geteld_record, telfouten
            if dimensie not in record:
                telfouten.append("Sleutel '{}' komt niet voor in record {}".format(dimensie, str(record)))
                return geteld_record, telfouten
            val = record.get(dimensie)
            if val in cds:
                if niv[cds.index(val)] == aggniv:
                    for key, val in record.items():
                        if key == dimensie:
                            # voeg dimensie toe met de code van de parent
                            parentcode = ptc[cds.index(val)]
                            pval = parentcode if not parentcode == '' else 'Totaal ' + key
                            geteld_record.update({key: pval})
                        elif key == 'sub_' + dimensie:
                            geteld_record.update({key: val})
                        elif key in vastedimensies:
                            # neem de 'vaste' keys over met de eigen code
                            geteld_record.update({key: val})
                        elif key == NUMGETELD_KEY:
                            # administatie: aantal keren dat het record is geteld
                            geteld_record.update({key: val+1})
                    if NUMGETELD_KEY not in geteld_record:
                        geteld_record.update({NUMGETELD_KEY: 1})
                    subkey = 'sub_' + dimensie
                    if subkey not in geteld_record:
                        geteld_record.update({subkey: record.get(dimensie)})

                    # Markeer record als aggregaat zijnde
                    geteld_record[IS_TUSSENTOTAAL] = True
            else:
                # code komt niet voor in de codelijst
                # N.B. dit zou eigenlijk niet mogen voorkomen
                # omdat we eerder een codelijst check hebben uitgevoerd
                if NUMGETELD_KEY not in record:
                    record_kort = dict()
                    for k, v in record.items():
                        if k == dimensie or k in vastedimensies:
                            record_kort.update({k: v})
                    telfouten.append("Code '{}' in record {} niet gevonden in codelijst.".format(val, str(record_kort)))
            return geteld_record, telfouten

        if record:
            # voeg record toe aan de lijst
            recs.append(record)
            # tel record 1 niveau omlaag (= naar bovenliggend record) voor de gekozen dimensie
            record, telfouten = tel_record(record, dimensie, vastedims, aggniveau, cds, niv, ptc)
            # voeg eventuele fouten toe
            errs.extend(telfouten)
            # we gaan 1 niveau omlaag (= omhoog in de codelijst)
            aggniveau = aggniveau - 1
            # aggregeer het bovenliggende record (recursie)
            aggregeren_record(recs, errs, record, dimensie, vastedims, aggniveau, cds, niv, ptc)

        return recs, errs

    # de MAIN loop waarin de door de data lopen
    # ieder record uit de data wordt geaggregeerd
    for index, record in enumerate(data):
        # ieder record (dict) uit data aggregeren
        aggrecords, fouten_agg = aggregeren_record([], [], record, dimensie, vastedims, aggniveau, cds, niv, ptc)

        if aggrecords:
            if len(aggrecords) == 1:
                # indien 1 record terug, dan is deze 'niet geteld'
                aggrecords[0].update({GETELD_KEY: False})
            else:
                # indien meer dan 1 record terug, dan zijn deze GETELD_KEY
                # tenzij deze in een eerdere aggregatie 'niet geteld' zijn
                for rec in aggrecords:
                    if GETELD_KEY not in rec:
                        rec.update({GETELD_KEY: True})
                    else:
                        geteld = rec.get(GETELD_KEY)
                        # record alleen als GETELD_KEY aanmerken
                        # indien eerder ook geteld (beide True)
                        geteld = geteld and True
                        rec.update({GETELD_KEY: geteld})

            if alleen_geteld is True:
                # alleen getelde records teruggeven
                for rec in aggrecords:
                    if rec.get(GETELD_KEY) is True:
                        # enkel element toevoegen: append
                        agg_data.append(rec)
            else:
                # alle elementen uit list toevoegen: extend
                agg_data.extend(aggrecords)
        # fouten toevoegen aan foutenlijst
        fouten.extend(fouten_agg)

    return agg_data, fouten
