import unittest

from http import HTTPStatus
import requests

from config.configurations import OSF_API_GEEF_FOUTEN_URL, OSF_API_GEEF_TOTALEN_UITKOMST_URL


class TestOSF_GeefTotalenUitkomstURL(unittest.TestCase):
    def setUp(self):
        self.osf_url = OSF_API_GEEF_TOTALEN_UITKOMST_URL

    def test_zonder_bestand_geeft_http500(self):
        response = requests.post(self.osf_url)

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code,
                         "De HTTP statuscode van de response is niet gelijk aan 500: INTERNAL_SERVER_ERROR.")

    @unittest.skip("Test overgeslagen omdat OSF deze functionaliteit nog niet in de API aanbiedt.")
    def test_bestand_zonder_fouten_geeft_http200(self):
        bestand = "test_bestanden/iv3_bestand_zonder_fouten_1.json"

        f = open(bestand, 'rb')
        bestanden = {'file': f}
        response = requests.post(self.osf_url, files=bestanden)

        f.close()

        self.assertEqual(HTTPStatus.OK, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 200: Ok.")

    def test_bestand_anders_dan_JSON_geeft_http500_en_fout(self):
        fouten_element_referentie = \
            [{'foutcode': 'SF999', 'melding': 'Onjuiste extensie', 'omschrijving': 'er is een algemene fout'}]
        bestand = "test_bestanden/dummy.txt"
        f = open(bestand, 'rb')
        bestanden = {'file': f}

        response = requests.post(self.osf_url, files=bestanden)
        response_json_format = response.json()

        f.close()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code,
                         "De HTTP statuscode van de response is niet gelijk aan 500: INTERNAL_SERVER_ERROR.")

        fouten_element = response_json_format["fouten"]

        self.assertEqual(fouten_element_referentie, fouten_element,
                         "Het fouten-element in het bestand bij de response is niet zoals verwacht.")

    def test_controle_geef_totalen_uitkomst_voor_bestand_met_DF(self):
        fouten_element_referentie = \
            ['Codefout in [data]:[lasten] record #0: taakveld 1.9 komt niet voor in de '"codelijst voor 'taakveld'",
             'Samenvatting: totaal 1 fouten gevonden op basis van codelijst controle.']

        bestand = "test_bestanden/iv3_bestand_definitie_fout.json"
        f = open(bestand, 'rb')
        bestanden = {'file': f}

        response = requests.post(self.osf_url, files=bestanden)
        response_json_format = response.json()
        fouten_element = response_json_format["fouten"]

        f.close()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code,
                         "De HTTP statuscode van de response is niet gelijk aan 500: INTERNAL_SERVER_ERROR.")
        self.assertEqual(fouten_element_referentie, fouten_element,
                         "Het fouten-element bij de response bevat geen definitiefout, terwijl dit wel zou moeten.")

    def test_controle_geef_totalen_uitkomst_voor_bestand_met_SF(self):
        fouten_element_referentie = \
            ["Fout #1: properties, data, required : 'lasten' is a required property",
             "Samenvatting: totaal 1 unieke fouten gevonden op basis van schema controle."]

        bestand = "test_bestanden/iv3_bestand_schema_fout.json"
        f = open(bestand, 'rb')
        bestanden = {'file': f}

        response = requests.post(self.osf_url, files=bestanden)
        response_json_format = response.json()
        fouten_element = response_json_format["fouten"]

        f.close()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code,
                         "De HTTP statuscode van de response is niet gelijk aan 500: INTERNAL_SERVER_ERROR.")
        self.assertEqual(fouten_element_referentie, fouten_element,
                         "Het fouten-element bij de response bevat geen schemafout, terwijl dit wel zou moeten.")

    def test_controle_geef_totalen_uitkomst_voor_bestand_met_PF(self):
        fouten_element_referentie = \
            [{'fout': 100.0,
              'foutcode': 'PF001',
              'goed': 1.0,
              'melding': 'Het saldo niet-financiële rekening niet gelijk aan het saldo van '
                         'de financiële rekening. Het gevonden percentage is 100.0, '
                         'terwijl 1.0 maximaal is toegestaan.',
              'omschrijving': 'Controle 1 onvoldoende'},
             {'fout': 16.87846280796888,
              'foutcode': 'PF002',
              'goed': 1.0,
              'melding': 'Gebruik juiste categorieën (6.1 en 7.5) op financiële balans. '
                         'Het gevonden percentage is 16.87846280796888, terwijl 1.0 '
                         'maximaal is toegestaan.',
              'omschrijving': 'Controle 2 onvoldoende'}]

        bestand = "test_bestanden/iv3_bestand_plausibiliteits_fout.json"
        f = open(bestand, 'rb')
        bestanden = {'file': f}

        response = requests.post(self.osf_url, files=bestanden)
        response_json_format = response.json()
        fouten_element = response_json_format["fouten"]

        f.close()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code,
                         "De HTTP statuscode van de response is niet gelijk aan 500: INTERNAL_SERVER_ERROR.")
        self.assertEqual(fouten_element_referentie, fouten_element,
                         "Het fouten-element bij de response bevat geen plausibiliteitsfout, terwijl dit wel zou moeten.")


class TestOSF_GeefFoutenURL(TestOSF_GeefTotalenUitkomstURL):
    def setUp(self):
        self.osf_url = OSF_API_GEEF_FOUTEN_URL
