import unittest

import requests
from config.configurations import OSF_API_GEEF_FOUTEN_URL, OSF_API_GEEF_TOTALEN_UITKOMST_URL


class BaseTest:
    class TestBaseOSFAPI(unittest.TestCase):
        def test_zonder_bestand_geeft_http500(self):
            response = requests.post(self.osf_url)

            self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")


        @unittest.skip("Test overgeslagen omdat OSF deze functionaliteit nog niet in de API aanbiedt.")
        def test_bestand_zonder_fouten_geeft_http200(self):
            bestand = "test_bestanden/iv3_bestand_zonder_fouten_1.json"

            f = open(bestand, 'rb')
            bestanden = {'file': f}
            response = requests.post(self.osf_url, files=bestanden)

            f.close()

            self.assertEqual(200, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 200.")


        def test_bestand_anders_dan_JSON_geeft_http500_en_fout(self):
            fouten_element_referentie = \
                [{'foutcode': 'SF999', 'melding': 'Onjuiste extensie', 'omschrijving': 'er is een algemene fout'}]
            bestand = "test_bestanden/dummy.txt"
            f = open(bestand, 'rb')
            bestanden = {'file': f}

            response = requests.post(self.osf_url, files=bestanden)
            response_json_format = response.json()

            f.close()

            self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")

            fouten_element = response_json_format["fouten"]

            self.assertEqual(fouten_element_referentie, fouten_element,
                             "Het fouten-element in het bestand bij de response is niet zoals verwacht.")


        def test_bestand_met_fouten_geeft_http500_en_fouten(self):
            fouten_element_referentie = \
                ["Fout #1: properties, contact, required : 'email' is a required property",
                 'Fout #2: properties, contact, additionalProperties : Additional properties '
                 "are not allowed ('e-mail' was unexpected)",
                 "Fout #3: properties, metadata, required : 'details_openbaar' is a required "
                 'property',
                 "Fout #4: properties, metadata, required : 'financieel_pakket' is a required "
                 'property',
                 "Fout #5: properties, metadata, required : 'export_software' is a required "
                 'property',
                 "Fout #6: properties, metadata, properties, boekjaar, type : '2018' is not of "
                 "type 'number'",
                 "Fout #7: properties, metadata, properties, datum, pattern : '6-3-2019' does "
                 'not match '
                 "'(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\\\[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'",
                 "Fout #8: properties, metadata, properties, periode, type : '1' is not of "
                 "type 'number'",
                 "Fout #9: properties, metadata, properties, periode, oneOf : '1' is not valid "
                 'under any of the given schemas',
                 "Subfout #9.1: 0, enum : '1' is not one of [0, 1, 2, 3, 4, 5]",
                 'Samenvatting: totaal 9 unieke fouten gevonden op basis van schema controle.']

            bestand = "test_bestanden/voorbeeld_geeft_schema_fouten.json"
            f = open(bestand, 'rb')
            bestanden = {'file': f}

            response = requests.post(self.osf_url, files=bestanden)
            response_json_format = response.json()
            fouten_element = response_json_format["fouten"]

            f.close()

            self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")
            self.assertEqual(fouten_element_referentie, fouten_element,
                             "Het fouten-element in het bestand bij de response is niet zoals verwacht.")


        # def test_controle_geef_totalen_uitkomst_voor_bestand_met_DF(self):
        #     fouten_element_referentie =
        #
        #     bestand = "test_bestanden/iv3_bestand_definitie_fout.json"
        #     f = open(bestand, 'rb')
        #     bestanden = {'file': f}
        #
        #     response = requests.post(self.osf_url, files=bestanden)
        #     response_json_format = response.json()
        #     fouten_element = response_json_format["fouten"]
        #
        #     f.close()
        #
        #     self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")
        #     self.assertEqual(fouten_element_referentie, fouten_element,
        #                      "Het fouten-element bij de response bevat geen definitiefout, terwijl dit wel zou moeten.")


        # def test_controle_geef_totalen_uitkomst_voor_bestand_met_SF(self):
        #     fouten_element_referentie =
        #
        #     bestand = "test_bestanden/iv3_bestand_schema_fout.json"
        #     f = open(bestand, 'rb')
        #     bestanden = {'file': f}
        #
        #     response = requests.post(self.osf_url, files=bestanden)
        #     response_json_format = response.json()
        #     fouten_element = response_json_format["fouten"]
        #
        #     f.close()
        #
        #     self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")
        #     self.assertEqual(fouten_element_referentie, fouten_element,
        #                      "Het fouten-element bij de response bevat geen schemafout, terwijl dit wel zou moeten.")


        # def test_controle_geef_totalen_uitkomst_voor_bestand_met_PF(self):
        #     fouten_element_referentie =
        #
        #     bestand = "test_bestanden/iv3_bestand_plausibiliteits_fout.json"
        #     f = open(bestand, 'rb')
        #     bestanden = {'file': f}
        #
        #     response = requests.post(self.osf_url, files=bestanden)
        #     response_json_format = response.json()
        #     fouten_element = response_json_format["fouten"]
        #
        #     f.close()
        #
        #     self.assertEqual(500, response.status_code, "De HTTP statuscode van de response is niet gelijk aan 500.")
        #     self.assertEqual(fouten_element_referentie, fouten_element,
        #                      "Het fouten-element bij de response bevat geen plausibiliteitsfout, terwijl dit wel zou moeten.")


        def test_controle_met_defbestand_extern(self):
            # json_bestand =
            #
            # controle_met_defbestand_extern()
            #
            # codefouten = []

            # api_url = 'https://cbs.openstate.eu/geef_totalen_uitkomst'
            #
            # response = requests.post(api_url)

            # with open(json_bestand, 'rb') as f:

            # response = requests.post(api_url, files={json_bestand: f})

            self.assertTrue(False, "Deze test moet nog geimplementeerd worden.")


class TestGeefFoutenURL(BaseTest.TestBaseOSFAPI):
    def setUp(self) -> None:
        self.osf_url = OSF_API_GEEF_FOUTEN_URL


class TestGeefTotalenUitkomstURL(BaseTest.TestBaseOSFAPI):
    def setUp(self) -> None:
        self.osf_url = OSF_API_GEEF_TOTALEN_UITKOMST_URL