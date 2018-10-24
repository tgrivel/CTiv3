import json
from collections import OrderedDict
#from Verwerking.maak_matrix import ItemTable
from flask_table import Table, Col


def ophalen_file(bestand):
    print (bestand.filename)
    newfile = bestand.read()
    try:
        data = json.loads(newfile.decode('utf-8'), object_pairs_hook=OrderedDict)
        print('verwerken als utf8')
    except:
        data = json.loads(newfile.decode('cp1251'), object_pairs_hook=OrderedDict)
        print('verwerken als cp1251')
    metadata = verwerken(data)
    return metadata

def verwerken(data):
    meta = data["metadata"]
    # aantal = 0
    # for row in data:
    #     aantal += 1
    # print('totaal ' + str(aantal) + ' ingelezen')
    return meta

