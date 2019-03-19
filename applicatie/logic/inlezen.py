import http
import json
from collections import OrderedDict
import urllib.request
from json import JSONDecodeError
from typing import Iterable
from urllib.error import URLError, HTTPError
import logging
from flask_table import Table, Col


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
            foutmeldingen.append(f"{bestand} is geen json-bestand")
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
    bestand, foutmeldingen = laad_json_bestand(jsonbestand)

    if not foutmeldingen:
        if not 'balans_lasten' in bestand['data']:
            bestand['data'].update({'balans_lasten':[]})
        if not 'balans_baten' in bestand['data']:
            bestand['data'].update({'balans_baten':[]})
        if not 'balans_standen' in bestand['data']:
            bestand['data'].update({'balans_standen':[]})

    return bestand, foutmeldingen


def ophalen_bestand_van_repo(url, bestandsnaam, bestandstype):
    """Haal json bestand van repo op.

     Geef json-bestand terug of een lijst met foutmeldingen.
     """
    url = url + bestandsnaam
    foutmeldingen = []
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
            _logger.info("json bestand opgehaald van %s", url)
    else:
        errormessage = 'Fout bij ophalen {0}: {1} (foutcode #{2})'.format(bestandstype, bestandsnaam, errorcode)
        foutmeldingen.append(errormessage)
        _logger.info("Fout bij ophalen Iv3-definitiebestand")

    # TODO Valideren met schema en foutmeldingen aanvullen

    return inhoud_bestand, foutmeldingen
