import http
import json
import logging
import urllib.request
from collections import OrderedDict
from json import JSONDecodeError
from urllib.error import URLError, HTTPError
from applicatie.logic.controles import controle_met_schema
from config.configurations import IV3_REPO_PATH, IV3_SCHEMA_FILE

_logger = logging.getLogger(__file__)


def ophalen_en_controleren_databestand(jsonbestand):
    """
    Haal JSON-bestand op. Voer controles uit.
    Geef JSON-bestand terug of een lijst met foutmeldingen.
    De volgende stappen worden doorlopen:
        - json data bestand inlezen
        - json schema ophalen van web
        - json data controleren aan json schema
    """

    # json bestand inlezen
    data_bestand, fouten = laad_json_bestand(jsonbestand)

    if not fouten:
        # json schema ophalen van web
        versie = "2_0"
        bestandsnaam = IV3_SCHEMA_FILE.format(versie)
        schema_bestand, fouten = ophalen_bestand_van_web(IV3_REPO_PATH, bestandsnaam, 'schemabestand')

    # json data controleren aan json schema
    if not fouten:
        fouten = controle_met_schema(data_bestand, schema_bestand)

    # json bestand voldoet aan het schema
    # echter balans_lasten, balans_baten en/of balans_standen kunnen ontbreken
    # in dit geval voegen we deze toe als lege dict
    if not fouten:
        if 'balans_lasten' not in data_bestand['data']:
            data_bestand['data'].update({'balans_lasten': []})
        if 'balans_baten' not in data_bestand['data']:
            data_bestand['data'].update({'balans_baten': []})
        if 'balans_standen' not in data_bestand['data']:
            data_bestand['data'].update({'balans_standen': []})

    return data_bestand, fouten


def laad_json_bestand(bestand):
    """Laad een json bestand. Het bestand kan gecodeerd zijn als utf-8 of als cp1252."""
    newfile = bestand.read()
    data = None
    foutmeldingen = []

    # Vind een geschikte encoding
    encodings = ['utf-8', 'cp1252']

    for encoding in encodings:
        try:
            data = json.loads(newfile.decode(encoding), object_pairs_hook=OrderedDict)
            _logger.info(f'verwerken als {encoding}')
            break
        except UnicodeDecodeError:
            continue  # Probeer de volgende
        except JSONDecodeError as e:
            foutmeldingen.append(f"{bestand.filename} is geen json-bestand")
            foutmeldingen.append("Fout gevonden op regel {}, kolom {}".format(e.lineno, e.colno))
            break
    else:
        foutmeldingen.append('Het bestand kon niet gelezen worden. '
                             'Geef een geschikt json-bestand.')

    return data, foutmeldingen


def ophalen_bestand_van_web(url, bestandsnaam, bestandstype):
    """Haal JSON-bestand van website op.

     Geef JSON-bestand terug of een lijst met foutmeldingen.
     """
    url = url + bestandsnaam
    weburl = None
    bestand = None
    errorcode = 0
    errortext = ''
    foutmeldingen = []

    try:
        req = urllib.request
        weburl = req.urlopen(url)
    except HTTPError as e:
        errorcode = e.code
        errortext = e.msg
    except URLError as e:
        if type(e.reason) is str:
            errortext = e.reason
        else:
            errortext = 'onbekende fout < {} >'.format(str(e.reason))
    except ValueError:
            errortext = 'onbekende fout < value error >'

    if errorcode == 0 and errortext == '':
        if weburl.getcode() == http.HTTPStatus.OK:
            bestand, foutmeldingen_json = laad_json_bestand(weburl)
            foutmeldingen.extend(foutmeldingen_json)
            _logger.info("JSON-bestand opgehaald van %s", url)
    else:
        foutmelding = 'Fout bij ophalen {}: {}'.format(bestandstype, bestandsnaam)
        foutmeldingen.append(foutmelding)
        if errorcode != 0:
            errortext = errortext.replace('Not Found', 'bestand niet gevonden')
            foutmelding = 'HTTP fout #{}: {}'.format(errorcode, errortext)
            foutmeldingen.append(foutmelding)
        elif errorcode == 0 and errortext != '':
            foutmelding = 'URL fout: {}'.format(errortext)
            foutmeldingen.append(foutmelding)

    if foutmeldingen:
        _logger.info("Fout bij ophalen van het {} met de naam: {}".format(bestandstype, bestandsnaam))

    return bestand, foutmeldingen
