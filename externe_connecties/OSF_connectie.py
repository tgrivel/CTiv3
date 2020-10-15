import requests


class OSF_connectie(object):
    """
    Regelt de aanroep naar de externe API van Open State Foundation (OSF).
    """
    def __init__(self):
        # self.respons = []
        # self.fouten = []
        pass

    # def geef_fouten(self):
    #     return self.fouten

    def geef_fouten(self): # json_bestand, api_url):
        """
        Zend JSON bestand naar OSF API waar controle plaatsvindt en die JSON bestand met fouten element terug stuurt.
        """
        # codefouten = []



        # json_bestand =
        api_url = 'https://cbs.openstate.eu/geef_totalen_uitkomst'



        # f = open(json_bestand, 'rb')
        # bestanden = {'file': f}

        # try:
        # response = requests.post(api_url, files=bestanden)
        response = requests.post(api_url)




        response_json_format = response.json()
        fouten_element = response_json_format["fouten"]
        print("regel 40 response geeft fouten_element: ", fouten_element)

        # except FileNotFoundError:
        #     print("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
        #     codefouten.append("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
        #     _logger.info("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")

        # f.close()

        # self.fouten = fouten_element

        # return codefouten
        # return fouten_element
        return response_json_format
