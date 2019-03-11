import http
import json
from collections import OrderedDict
import urllib.request
from urllib.error import URLError, HTTPError
import logging
from flask_table import Table, Col

datalastenbaten = {}

_logger = logging.getLogger(__file__)


def laad_json_bestand(bestand):
    """Laad een json bestand. Het bestand kan gecodeerd zijn als utf-8 of als cp1252."""
    newfile = bestand.read()
    try:
        data = json.loads(newfile.decode('utf-8'), object_pairs_hook=OrderedDict)
        _logger.info('verwerken als utf8')
    except UnicodeDecodeError:
        data = json.loads(newfile.decode('cp1251'), object_pairs_hook=OrderedDict)
        _logger.info('verwerken als cp1251')
    return data


def ophalen_definitiebestand(meta):
    ovlaag = meta['overheidslaag']
    boekjaar = meta['boekjaar']
    # tijdelijke oplossing:
    boekjaar = '2017'
    url = "https://raw.github.com/tgrivel/iv3_modellen/master/" + "iv3_definities_" + ovlaag + "_" + boekjaar + ".json"
    errorcode = 0
    try:
        webUrl = urllib.request.urlopen(url)
    except HTTPError as e:
        errorcode = e.code
    except URLError as e:
        errorcode = e.code
    if errorcode == 0:
        if webUrl.getcode() == http.HTTPStatus.OK:
            inhoud_bestand = laad_json_bestand(webUrl)
            _logger.info("Sjabloon opgehaald van %s", url)
    else:
        inhoud_bestand = 'Fout bij ophalen Iv3 definitiebestand (foutcode #{0})'.format(errorcode)
        _logger.info("Fout bij ophalen Iv3 definitiebestand")

    return inhoud_bestand



def verwerken(data):
    """Wat doet deze functie?

    Iets optellen en meta teruggeven?

    """
    meta = data["metadata"]
    records  = data["waarden"]
    totaal = 0
    for record in records:
        totaal += int(record['bedrag'])
    _logger.info("Aantal records %d", totaal)
    # aantal = 0
    # for row in data:
    #     aantal += 1
    # print('totaal ' + str(aantal) + ' ingelezen')
    return meta


def indikken_data(data):
    """"Wat is indikken??

    data zijn alleen de waarden
    """
    datalastenbaten = {}
    num_fouten = 0

    _logger.info('in indikken')
    for rec in data:
        try:
            kant = rec['rekeningkant']
            bedrag = rec['bedrag']
            # bedrag = float(rec['bedrag'].replace(',', '.'))
            if kant == 'Lasten' or kant == 'Baten':
                cat = rec['categorie']
                taakv = rec['taakveld']
                code = (kant, taakv, cat)
            elif kant == 'balans_baten' or kant == 'balans_lasten':
                cat = rec['categorie']
                bal_code = rec['balanscode']
                code = (kant, bal_code, cat)
            else:
                 stand_per = rec['standper']
                 bal_code = rec['balanscode']
                 code = ('balans_standen', bal_code, stand_per)

            if code in datalastenbaten:
                datalastenbaten[code] += bedrag
            else:
                datalastenbaten[code] = bedrag
        except:
            num_fouten = num_fouten + 1
            print('Fout {} in indikken'.format(num_fouten))
            for k,v in rec.items():
                pass
                #print (k,v)
    # print('export: ')
    # for k, v in datalastenbaten.items():
    #     print(k,v)
    return datalastenbaten


