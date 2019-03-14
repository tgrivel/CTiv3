import http
import json
from collections import OrderedDict
import urllib.request
from json import JSONDecodeError
from typing import Iterable
from urllib.error import URLError, HTTPError
import logging
from flask_table import Table, Col

datalastenbaten = {}

_logger = logging.getLogger(__file__)


def laad_json_bestand(bestand):
    """Laad een json bestand. Het bestand kan gecodeerd zijn als utf-8 of als cp1252."""
    newfile = bestand.read()
    data = None
    foutmeldingen = []

    # Vind een geschikte encoding
    encodings = ['utf8', 'cp1252']

    for encoding in encodings:
        try:
            data = json.loads(newfile.decode(encoding), object_pairs_hook=OrderedDict)
            _logger.info(f'verwerken als {encoding}')
            break
        except UnicodeDecodeError:
            continue  # Probeer de volgende
        except JSONDecodeError as e:
            foutmeldingen.append(f"{bestand} is geen JSON-bestand")
            break
    else:
        foutmeldingen.append('Het bestand kon niet gelezen worden. '
                             'Geef een geschikt json-bestand.')

    return data, foutmeldingen


def ophalen_databestand(jsonbestand):
    """Haal jsonbestand op.

    Geef json-bestand terug of een lijst met foutmeldingen.
    """

    # json bestand inlezen
    complete_upload, foutmeldingen = laad_json_bestand(jsonbestand)

    # TODO Valideren met schema en foutmeldingen aanvullen

    return complete_upload, foutmeldingen


def ophalen_definitiebestand(meta):
    foutmeldingen = []
    ovlaag = meta['overheidslaag']
    boekjaar = meta['boekjaar']
    bestandsnaam = 'iv3_definities_' + ovlaag + '_' + boekjaar + '.json'
    url = "https://raw.github.com/tgrivel/iv3_modellen/master/" + bestandsnaam

    inhoud_bestand = None
    errorcode = 0
    try:
        webUrl = urllib.request.urlopen(url)
    except HTTPError as e:
        errorcode = e.code
    except URLError as e:
        errorcode = e.code
    if errorcode == 0:
        if webUrl.getcode() == http.HTTPStatus.OK:
            inhoud_bestand, foutmeldingen_json = laad_json_bestand(webUrl)
            foutmeldingen.extend(foutmeldingen_json)
            _logger.info("Sjabloon opgehaald van %s", url)
    else:
        errormessage = 'Fout bij ophalen definitiebestand {0} (foutcode #{1})'.format(bestandsnaam, errorcode)
        foutmeldingen.append(errormessage)
        _logger.info("Fout bij ophalen Iv3 definitiebestand")

    # TODO Valideren met schema en foutmeldingen aanvullen

    return inhoud_bestand, foutmeldingen


