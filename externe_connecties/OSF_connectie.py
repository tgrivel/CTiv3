from config.configurations import OSF_API_GEEF_FOUTEN_URL

import requests
import logging
from applicatie.main.CustomExceptions import OSFAanroepError


_logger = logging.getLogger(__file__)


def osf_aanroep(jsonbestandsnaam):
    """Zend json-bestand naar OSF-api en ontvang gecontroleerd resultaat met fouten."""
    try:
        bestanden = {'file': open(jsonbestandsnaam)}
        response = requests.post(OSF_API_GEEF_FOUTEN_URL, files=bestanden)
    except FileNotFoundError as e:
        _logger.info("Het geuploade JSON bestand geeft een exception: Exception: {}".format(e))
        raise OSFAanroepError
    except requests.exceptions.RequestException as e:
        _logger.info("Exception bij het versturen van een JSON bestand naar de OSF API: Exception: {}".format(e))
        raise OSFAanroepError
    return response


def geef_fouten(jsonbestandsnaam):
    """Haalt fouten element uit response van osf_aanroep()."""
    response = osf_aanroep(jsonbestandsnaam)
    response_json_format = response.json()
    fouten_element = response_json_format["fouten"]
    return fouten_element
