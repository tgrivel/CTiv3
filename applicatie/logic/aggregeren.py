# logica voor aggregeren van data
import logging
from applicatie.logic.controles import geef_codechecklijst

_logger = logging.getLogger(__file__)


def aggregeren_volledig(data, defbestand):
    """"Volledige dataset aggregeren.
    Per rekening specificeren we de dimensies
    waarover geaggregeerd moet worden.
    """
    data_geaggregeerd = dict()
    fouten_aggregeren = list()

    cl = defbestand['codelijsten']
    codechecklijst = geef_codechecklijst(cl)

    # rekening lasten aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['lasten'],
        ['categorie', 2, 'categorie_lasten'],
        ['taakveld', 2, 'taakveld'],
        codechecklijst
    )
    data_geaggregeerd['lasten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # rekening balans_lasten aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['balans_lasten'],
        ['categorie', 2, 'categorie_lasten'],
        ['balanscode', 2, 'balanscode'],
        codechecklijst
    )
    data_geaggregeerd['balans_lasten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # rekening baten aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['baten'],
        ['categorie', 2, 'categorie_baten'],
        ['taakveld', 2, 'taakveld'],
        codechecklijst
    )
    data_geaggregeerd['baten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # rekening balans_baten aggregeren
    data_agg, fouten = aggregeren_rekening(
        data['balans_baten'],
        ['categorie', 2, 'categorie_baten'],
        ['balanscode', 2, 'balanscode'],
        codechecklijst
    )
    data_geaggregeerd['balans_baten'] = data_agg
    fouten_aggregeren.extend(fouten)

    # rekening balans_standen aggregeren
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
    """
    data voor een rekening volledig aggregeren over twee dimensies
    we specificeren hiervoor dimensie_1 en dimensie_2, dit zijn lists:
    [ naam dimensie, aggregatieniveau, naam codelijst ]
    """
    foutenlijst = list()

    # aggregeren over dimensie 1
    vastedims = [dimensie_2[0], 'bedrag']   # we houden de tweede dimensie vast
    aggdim, aggniv, clnaam = dimensie_1
    clijst = codechecklijst.get(clnaam)
    if aggniv > -1:
        data, fouten = aggregeren_data(data, aggdim, vastedims, aggniv, clijst, False)
        foutenlijst.extend(fouten)

    # aggregeren over dimensie 2
    vastedims = [dimensie_1[0], 'bedrag']   # we houden de eerste dimensie vast
    aggdim, aggniv, clnaam = dimensie_2
    clijst = codechecklijst.get(clnaam)
    data, fouten = aggregeren_data(data, aggdim, vastedims, aggniv, clijst, True)
    foutenlijst.extend(fouten)

    data = data_opschonen(data, ['geteld', 'numgeteld'])

    return data, foutenlijst


def aggregeren_data(data, dimensie, vastedimensies, aggniveau, clijst, alleen_geteld):
    """"
    aggregeren data: lijst van data records
    """
    # Laatste wijziging 24 maart 2019 (getest in Jupyter notebook)

    agg_data = list()
    fouten = list()

    if not clijst:
        fouten.append("Geen codelijst beschikbaar voor {}.".format(dimensie))
        return agg_data, fouten

    if aggniveau < 0:
        # stoppen indien aggregatieniveau negatief
        fouten.append("Aggregatieniveau mag niet negatief zijn.")
        return agg_data, fouten

    cds = clijst[0::4]  # cds: lijst van codes
    niv = clijst[2::4]  # niv: niveau van codes in de codelijst (0 = hoogste niveau)
    ptc = clijst[3::4]  # ptc: lijst van parent codes behorende bij de codes

    def aggregeren_record(recs, errs, record, dimensie, vastedimensies, aggniveau, cds, niv, ptc):
        """Recursieve functie om een record uit data 
        te aggregeren tot op het laagste niveau"""""

        def tel_record(record, dimensie, vastedimensies, aggniv, cds, niv, ptc):
            geteld_record = dict()
            telfouten = list()
            if aggniv == 0:
                # niveau waarop we stoppen met doortellen
                return geteld_record, telfouten
            if 'geteld' in record:
                # stoppen indien record eerder als 'niet geteld' is gemarkeerd
                if record.get('geteld') is False:
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
                            pval = ptc[cds.index(val)]
                            if pval == '':
                                pval = 'Totaal ' + key
                            geteld_record.update({key: pval})
                        elif key in vastedimensies:
                            # voeg overige 'vaste' keys toe met de eigen code
                            geteld_record.update({key: val})
                        elif key == 'numgeteld':
                            # houd bij hoevaak het record is geteld
                            geteld_record.update({key: val+1})
                    if 'numgeteld' not in geteld_record:
                        geteld_record.update({'numgeteld': 1})
            else:
                # code komt niet voor in de codelijst
                # N.B. dit zou eigenlijk niet mogen voorkomen
                # omdat we eerder een codelijst check hebben uitgevoerd
                if 'numgeteld' not in record:
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
            record, telfouten = tel_record(record, dimensie, vastedimensies, aggniveau, cds, niv, ptc)
            # voeg eventuele fouten toe
            errs.extend(telfouten)
            # we gaan 1 niveau omlaag (= omhoog in de codelijst)
            aggniveau = aggniveau - 1
            # aggregeer het bovenliggende record (recursie)
            aggregeren_record(recs, errs, record, dimensie, vastedimensies, aggniveau, cds, niv, ptc)

        return recs, errs

    # dit is de main loop waarin de door de data lopen
    for index, record in enumerate(data):
        # ieder record uit data aggregeren
        aggrecords, fouten_agg = aggregeren_record([], [], record, dimensie, vastedimensies, aggniveau, cds, niv, ptc)
        if aggrecords:
            if len(aggrecords) == 1:
                # indien 1 record terug, dan is deze 'niet geteld'
                aggrecords[0].update({'geteld': False})
            else:
                # indien meer dan 1 record terug, dan zijn deze 'geteld'
                # tenzij deze in een eerdere aggregatie 'niet geteld' zijn
                for rec in aggrecords:
                    if 'geteld' not in rec:
                        rec.update({'geteld': True})
                    else:
                        geteld = rec.get('geteld')
                        # record alleen als 'geteld' aanmerken
                        # indien eerder ook geteld (beide True)
                        geteld = geteld and True
                        rec.update({'geteld': geteld})
            if alleen_geteld is True:
                # alleen getelde records teruggeven
                for rec in aggrecords:
                    if rec.get('geteld') is True:
                        # enkel element toevoegen: append
                        agg_data.append(rec)
            else:
                # alle elementen uit list toevoegen: extend
                agg_data.extend(aggrecords)
        # fouten toevoegen aan foutenlijst
        fouten.extend(fouten_agg)

    return agg_data, fouten


def data_opschonen(data, keylist):
    # data is een list van records (dicts)
    # verwijder de opgegeven keys uit alle records

    data_schoon = [{k: v for (k, v) in record.items() if k not in keylist}
                   for record in data]

    return data_schoon
