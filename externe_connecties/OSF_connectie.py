# Hier komt de code voor de aanroep naar de externe API van Open State Foundation (OSF).


class OSF_connectie(object):
    def controle(json_bestand, api_url):
        """
        Controleer een JSON bestand op basis van definitiebestand; uitgevoerd in een externe API.
        """
        codefouten = []

        # api_url = 'https://cbs.openstate.eu/geef_totalen_uitkomst'

        f = open(json_bestand, 'rb')
        bestanden = {'file': f}

        # try:
        response = requests.post(api_url, files=bestanden)
        response_json_format = response.json()
        fouten_element = response_json_format["fouten"]
        print("regel 110 controle_met_defbestand_extern(): ", fouten_element)

        # except FileNotFoundError:
        #     print("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
        #     codefouten.append("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")
        #     _logger.info("Het geuploade json bestand bestaat niet of kan niet gevonden worden.")

        f.close()

        # Vind foutmeldingen voor gebruiker bij fouten uit fouten_element.
        codefouten = foutmeldingen_voor_gebruiker(fouten_element)

        return codefouten

    def foutmeldingen_voor_gebruiker(fouten_element):
        foutmeldingen = []

        # Lees in fouten bestand voor overzicht fouten en de meldingen voor de gebruiker.
        fouten_bestand, inlees_fouten = ophalen_bestand_van_web(IV3_REPO_PATH, "fouten.json", 'foutenbestand')
        print("regel 136: ", fouten_bestand[0])

        for fout in fouten_element:
            # Vind de foutmelding voor de gebruiker uit het fouten_bestand behorende bij de fout:

            foutmeldingen.append()

        return foutmeldingen