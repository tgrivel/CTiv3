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
    bestandsnaam = 'iv3_definities_' + ovlaag + '_' + boekjaar + '.json'
    url = "https://raw.github.com/tgrivel/iv3_modellen/master/" + bestandsnaam

    inhoud_bestand = object()
    errormessage = ''
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
        errormessage = 'Fout bij ophalen definitiebestand {0} (foutcode #{1})'.format(bestandsnaam, errorcode)
        _logger.info("Fout bij ophalen Iv3 definitiebestand")

    resultaat = [inhoud_bestand, errormessage]
    return resultaat


