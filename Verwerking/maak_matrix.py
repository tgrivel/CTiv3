# import things
from flask_table import Table, Col
from Verwerking.inlezen import verwerken


# header = {'kolkop':['1.0', '3.1','6.1','7.0']}
#
# data = {'regels':[['tv 1.0','','12','','123'],
#         ['tv 1.1','3','2','1','0'],
#         ['tv 2.0','','43','',''],
#         ['tv 6.6','4','','','13']]
#         }


def maak_tabel(compacte_data, afdeling, header, rijen):
    kolommen = header['kolkop']
    print(afdeling,kolommen)
    rijen = rijen['rijkop']
    data_tot = []
    for rij in rijen:
        data_rij = []
        data_rij.append(rij)
        for kolom in kolommen:
            combi_code = (afdeling, rij, kolom)
            if combi_code in compacte_data:
                data_rij.append(compacte_data[combi_code])
            else:
                data_rij.append('')
        print(data_rij)
        data_tot.append(data_rij)
    data = {'regels':data_tot}
    # print(data)
    return data

# def bouw_matrix_LR(subset_data):
#         kolkop = []
#         rijkop = []
#         bedrag =
#         for rec in subset_data:
#                 if rec["categorie"] not in kolkop:
#                         kolkop.append(rec["categorie"])
#                 if rec["taakveld"] not in rijkop:
#                         rijkop.append(rec["taakveld"])
#         for rec in
#         header = {'kolkop':kolkop}


def maak_lijst_koppen(sjabloon, kop_soort ):
    lijst_koppen = []
    selectie = sjabloon[kop_soort]
    if kop_soort == 'BalansDatums':
        for rec in selectie:
            lijst_koppen.append(rec['code'])
    else:
        for hfd_code in selectie:
            for rec in hfd_code['subcodes']:
                lijst_koppen.append(rec['code'])
    return lijst_koppen