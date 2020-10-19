from config.configurations import OSF_API_GEEF_FOUTEN_URL

import requests
import logging
from applicatie.main.CustomExceptions import OSFAanroepError


_logger = logging.getLogger(__file__)


def OSF_aanroep(jsonbestandsnaam):
    """
    Regelt de aanroep naar de externe API van Open State Foundation (OSF).
    Zend JSON bestand naar OSF API waar controle plaatsvindt en die JSON bestand met fouten element terug stuurt.
    """
    try:
        bestanden = {'file': open(jsonbestandsnaam)}
        response = requests.post(OSF_API_GEEF_FOUTEN_URL, files=bestanden)
        # response.raise_for_status() # Raise exceptions in case of HTTP errors.
    except FileNotFoundError as e:
        _logger.info("Het geuploade JSON bestand geeft een exception: Exception: {}".format(e))
        raise OSFAanroepError
    except requests.exceptions.RequestException as e:
        _logger.info("Exception bij het versturen van een JSON bestand naar de OSF API: Exception: {}".format(e))
        raise OSFAanroepError
    return response

def geef_fouten(jsonbestandsnaam):
    """
    Haalt fouten element uit response van OSF_aanroep(json_bestand).
    """
    response = OSF_aanroep(jsonbestandsnaam)
    response_json_format = response.json()
    fouten_element = response_json_format["fouten"]
    return fouten_element
