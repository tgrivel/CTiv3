# hieronder staan enkele stukje script waarmee
# geprobeerd is een opzet te mkaen met rekeken voor iv3
# stukjes kunnen wellicht gebruikt worden bij het maken van
# sub-totalen.
# het inlezen van werkelijke data tot een tabel is al
# geregeld in maak_matrix en inlezen

import json
from collections import OrderedDict
from models import LayoutLastenBaten, DataLastenBaten, TotalenLastenBaten,  PaginaDefinities


pagdefs = []
hierarchie = []
dict_hierarchie = {}
datalastenbaten = {}
totalen = {}

def inlezen():
    # global pagdefs
    global hierarchie
    sjabloon_bestand = r'C:\Theo\werk\GemJson\iv3_modellen\iv3_codes_2018_gemeente_aangep.json'
    with open(sjabloon_bestand) as bron:
        data = json.load(bron, object_pairs_hook=OrderedDict)
        import_typen = data['Rekeningkanten']
        hierarchie_lijstje = vul_code_hierarchie(import_typen, data)
        pagina_definities = geef_pagina_definities(import_typen)
        # print ('data inlezen en tellen')
        # gevulde_data_tabel = \
        vul_data_tabel()
        # for c,b in gevulde_data_tabel.items():
        #     print (f"{c} = {b}")
        # print('Nu gaan we totalen tellen')
        totalen_tellen()

        # geef_pagina_definities(import_typen)
    # for rec in pagdefs:
    #     print(rec)


def totalen_tellen():
    global datalastenbaten
    global dict_hierarchie
    global totalen
    # print ('aantal records:', len(datalastenbaten))
    for sleutel, waarde in datalastenbaten.items():
        # print ('record voor totaal: ', rec)
        kant = sleutel[0]
        taakv = sleutel[1]
        cat = sleutel[2]
        bedrag = waarde
        if kant == 'lasten':
            catsoort = 'LastenCategorien'
        elif kant == 'baten':
            catsoort = 'BatenCategorien'
        parent_taakv = dict_hierarchie[(kant,'Taakvelden',taakv)]
        parent_cat = dict_hierarchie[(kant,catsoort,cat)]

        nwe_combi_tv = (kant,parent_taakv,cat)
        if nwe_combi_tv in totalen:
            totalen[nwe_combi_tv] += bedrag
        else:
            totalen[nwe_combi_tv] = bedrag
        # print(kant, taakv, cat, bedrag, 'parent', parent_taakv)
        nwe_combi_c = (kant, taakv, parent_cat)
        if nwe_combi_c in totalen:
            totalen[nwe_combi_c] += bedrag
        else:
            totalen[nwe_combi_c] = bedrag
        nwe_combi_tot = (kant,parent_taakv,parent_cat)
        if nwe_combi_tot in totalen:
            totalen[nwe_combi_tot] += bedrag
        else:
            totalen[nwe_combi_tot] = bedrag

    for k,v in totalen.items():
        print("{k} = {v}")
    hoogste_niveau_tellen(totalen)

def hoogste_niveau_tellen(totalen):
    global dict_hierarchie
    totaaltjes = {}
    for k,v in totalen.items():
        totaaltjes[k]=v
    # print('aantal records totaaltjes:', len(totaaltjes))
    for sleutel, waarde in totaaltjes.items():
        # print ('record voor totaal: ', rec)
        kant = sleutel[0]
        taakv = sleutel[1]
        cat = sleutel[2]
        bedrag = waarde
        if kant == 'lasten':
            catsoort = 'LastenCategorien'
        elif kant == 'baten':
            catsoort = 'BatenCategorien'
        parent_taakv = dict_hierarchie[(kant, 'Taakvelden', taakv)]
        parent_cat = dict_hierarchie[(kant, catsoort, cat)]

        nwe_combi_tv = (kant, parent_taakv, cat)
        if nwe_combi_tv in totalen:
            totalen[nwe_combi_tv] += bedrag
        else:
            totalen[nwe_combi_tv] = bedrag
        # print(kant, taakv, cat, bedrag, 'parent', parent_taakv)

        nwe_combi_c = (kant, taakv, parent_cat)
        if nwe_combi_c in totalen:
            totalen[nwe_combi_c] += bedrag
        else:
            totalen[nwe_combi_c] = bedrag

        # nwe_combi_tot = (kant, parent_taakv, parent_cat)
        # if nwe_combi_tot in totalen:
        #     totalen[nwe_combi_tot] += bedrag
        # else:
        #     totalen[nwe_combi_tot] = bedrag

    for k, v in totalen.items():
        print("{k[0]}; {k[1]} ;{k[2]} ; {v}")




def vul_data_tabel():
    global datalastenbaten
    # nwe_datalastenbaten = DataLastenBaten
    bron_bestand = r'C:\Theo\werk\GemJson\json_testbestanden\KRDenkele_records.json'
    with open(bron_bestand) as bron_data:
        bron = json.load(bron_data)
        data = bron['waarden']
        nr = 0
        for rec in data:
            nr += 1
            kant = rec['rekeningkant']
            if kant == 'lasten' or kant == 'baten':
                cat = rec['categorie']
                taakv = rec['taakveld']
                code = (kant,taakv, cat)
                bedrag = float(rec['bedrag'].replace(',','.'))
                if code in datalastenbaten:
                    datalastenbaten[code] +=bedrag
                else:
                    datalastenbaten[code] = bedrag
        # print ('toaal aantal records bron : ' + str(nr))
    for k, v in datalastenbaten.items():
        print("{k[0]}; {k[1]} ;{k[2]} ; {v}")
    return datalastenbaten


def vul_code_hierarchie(import_typen, data):
    global dict_hierarchie
    lst_codelijsten = []
    for rec in import_typen:     # hier loopt hij door de sleutel en de 3 typen heen: lasten, baten, balans
        if 'code' in rec.keys():   # alleen nog de 3 typen
            type = rec['code'].lower()      # hier wordt vastgelegd met welk type we bezig zijn
            inhoud = rec['contents']  # per type lopen we door de rijen en kolommen heen
            codelst = ''
            for rijkol in inhoud:
                if 'Rijen' in rijkol.keys():
                    codelst = type ,'Rijen', rijkol['Rijen']
                if 'Kolommen' in rijkol.keys():
                    codelst =  type, 'Kolommen',rijkol['Kolommen']
                if codelst != '':
                    # print('eentje toeveogen aan lst_codeslijsten: ', codelst)
                    lst_codelijsten.append(codelst)
    for codelijst in lst_codelijsten: # nu hebben we een lijst met unieke codelijst namen, kunnen we daardoorheen
        rekeningkant = codelijst[0]
        rij_of_kolom = codelijst[1]
        codelijst = codelijst[2]
        print(rekeningkant, rij_of_kolom,codelijst)
        records_codelijst = data[codelijst]
        # print('we zijn hier')
        for hfd_codes in records_codelijst:
            code_hfd_code = hfd_codes['code']
            if 'subcodes' in hfd_codes.keys():
                # print('hebbes')
                subcodes = hfd_codes['subcodes']
                for regel in subcodes:
                    # print (regel)
                    code = regel['code']
                    # print(code)
                    combi_child = (rekeningkant, codelijst, code)
                    dict_hierarchie[combi_child]=code_hfd_code
            combi_child = (rekeningkant, codelijst, code_hfd_code)
            dict_hierarchie[combi_child] = 'Totaal ' + codelijst
        combi_child = (rekeningkant, codelijst, 'Totaal ' + codelijst)
        dict_hierarchie[combi_child] = 'Totaal '+ rij_of_kolom + ' ' + rekeningkant
    print('overzicht hierarchie dict')
    for k,v in dict_hierarchie.items():
        print("{k} = {v}")

def voeg_pagina_definities_toe(rekeningkant, kolomgroep, rijgroep):
    global pagdefs
    nieuw = PaginaDefinities(rekeningkant,kolomgroep,rijgroep)
    pagdefs.append(nieuw)


def geef_pagina_definities(import_typen):
    for rec in import_typen:
        # print(rec.keys())
        if 'Code' in rec.keys():
            if rec['Code'] == 'Lasten':
                lst_rijgroep_lasten = []
                lst_kolomgroep_lasten = []
                for inhoud in rec['inhoud']:
                    if 'Rijen' in inhoud.keys():
                        lst_rijgroep_lasten.append(inhoud['Rijen'])
                    if 'Kolommen' in inhoud.keys():
                        lst_kolomgroep_lasten.append(inhoud['Kolommen'])
            voeg_pagina_definities_toe('Lasten', lst_kolomgroep_lasten, lst_rijgroep_lasten)
            # print ('nu gaan we baten doen')
            if rec['Code'] == 'Baten':
                lst_rijgroep_baten = []
                # print('1')
                lst_kolomgroep_baten = []
                for inhoud in rec['inhoud']:
                    if 'Rijen' in inhoud.keys():
                        lst_rijgroep_baten.append(inhoud['Rijen'])
                    if 'Kolommen' in inhoud.keys():
                        lst_kolomgroep_baten.append(inhoud['Kolommen'])
                        # print('joehoe' + inhoud['Kolommen'])
                # print( lst_kolomgroep_baten, lst_rijgroep_baten)
                voeg_pagina_definities_toe('Baten',lst_kolomgroep_baten, lst_rijgroep_baten)
            if rec['Code'] == 'Balans':
                lst_rijgroep_balans = []
                lst_kolomgroep_balans = []
                volgnr = 0
                for inhoud in rec['inhoud']:
                    if 'Rijen' in inhoud.keys():
                        lst_rijgroep_balans.append(inhoud['Rijen'])
                    if 'Kolommen' in inhoud.keys():
                        lst_kolomgroep_balans.append(inhoud['Kolommen'])
                voeg_pagina_definities_toe('Balans',lst_kolomgroep_balans, lst_rijgroep_balans)
    return


if __name__ == "__main__":
    inlezen()