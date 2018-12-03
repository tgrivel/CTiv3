import json
from collections import OrderedDict
import os
import urllib.request
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
    records  = data["waarden"]
    totaal = 0
    for record in records:
        totaal += int(record['bedrag'])
    print(totaal)
    # aantal = 0
    # for row in data:
    #     aantal += 1
    # print('totaal ' + str(aantal) + ' ingelezen')
    return meta


def ophalen_sjabloon(meta):
    # print(bestand.filename)
    metadata = []
    ovlaag = meta['overheidslaag']
    boekjaar = meta['boekjaar']
    # naam_sjabloon = 'C:\Theo\werk\CTiv3\sjablonen\iv3Codes' + ovlaag + boekjaar + '.json'
    url = "https://raw.github.com/tgrivel/iv3_modellen/master/" + "iv3Codes" + ovlaag + boekjaar + ".json"
    print(url)
    webUrl = urllib.request.urlopen(url)
    if (webUrl.getcode() == 200):
        bestand = webUrl.read()
        try:
            data = json.loads(bestand.decode('utf-8'), object_pairs_hook=OrderedDict)
            print('verwerken als utf8')
        except:
            data = json.loads(bestand.decode('cp1251'), object_pairs_hook=OrderedDict)
            print('verwerken als cp1251')
        metadata = verwerken_sjabloon(data)
    return metadata

def verwerken_sjabloon(sjabloon_bestand):
    meta = sjabloon_bestand["metadata"]
    return meta