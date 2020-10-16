from config.configurations import OSF_API_GEEF_FOUTEN_URL

import requests


def OSF_aanroep(jsonbestandsnaam):
    """
    Regelt de aanroep naar de externe API van Open State Foundation (OSF).
    Zend JSON bestand naar OSF API waar controle plaatsvindt en die JSON bestand met fouten element terug stuurt.
    """
    bestanden = {'file': open(jsonbestandsnaam)}

    # try:
    response = requests.post(OSF_API_GEEF_FOUTEN_URL, files=bestanden)

    # except FileNotFoundError:
    #     print("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
    #     codefouten.append("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
    #     _logger.info("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
    return response

def geef_fouten(jsonbestandsnaam):
    """
    Haalt fouten element uit response van OSF_aanroep(json_bestand).
    """
    response = OSF_aanroep(jsonbestandsnaam)
    response_json_format = response.json()
    fouten_element = response_json_format["fouten"]
    return fouten_element
