from config.configurations import OSF_API_GEEF_TOTALEN_UITKOMST_URL

import requests


def OSF_aanroep(json_bestand):
    """
    Regelt de aanroep naar de externe API van Open State Foundation (OSF).
    Zend JSON bestand naar OSF API waar controle plaatsvindt en die JSON bestand met fouten element terug stuurt.
    """
    # codefouten = []



    # json_bestand =



    f = open(json_bestand, 'rb')
    bestanden = {'file': f}

    # try:
    response = requests.post(OSF_API_GEEF_TOTALEN_UITKOMST_URL, files=bestanden)
    # response = requests.post(OSF_API_GEEF_TOTALEN_UITKOMST_URL)




    # response_json_format = response.json()
    # fouten_element = response_json_format["fouten"]
    # print("regel 40 response geeft fouten_element: ", fouten_element)

    # except FileNotFoundError:
    #     print("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
    #     codefouten.append("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
    #     _logger.info("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")

    f.close()

    # self.fouten = fouten_element

    # return codefouten
    return response

def geef_fouten(json_bestand):
    """
    Haalt fouten element uit response van OSF_aanroep(json_bestand).
    """
    response = OSF_aanroep(json_bestand)
    response_json_format = response.json()
    fouten_element = response_json_format["fouten"]
    return fouten_element
