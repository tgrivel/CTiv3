import json
from collections import OrderedDict
import urllib.request
from flask_table import Table, Col


HTTP_OKAY = 200


def laad_json_bestand(bestand):
    """Laad een json bestand.

    Het bestand kan gecodeerd zijn als utf-8 of als cp1252.
    """

    newfile = bestand.read()
    try:
        data = json.loads(newfile.decode('utf-8'), object_pairs_hook=OrderedDict)
        print('verwerken als utf8')
    except UnicodeDecodeError:
        data = json.loads(newfile.decode('cp1251'), object_pairs_hook=OrderedDict)
        print('verwerken als cp1251')
    return data


def ophalen_sjabloon(meta):
    metadata = []
    ovlaag = meta['overheidslaag']
    boekjaar = meta['boekjaar']
    # naam_sjabloon = 'C:\Theo\werk\CTiv3\sjablonen\iv3Codes' + ovlaag + boekjaar + '.json'
    url = "https://raw.github.com/tgrivel/iv3_modellen/master/" + "iv3Codes" + ovlaag + boekjaar + ".json"
    print(url)
    webUrl = urllib.request.urlopen(url)
    if (webUrl.getcode() == HTTP_OKAY):
        # bestand = webUrl.read()
        metadata = laad_json_bestand(webUrl)

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
