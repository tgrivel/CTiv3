from unittest import TestCase
from unittest.mock import Mock, patch

from applicatie.main.custom_exceptions import OSFAanroepError
from externe_connecties.OSF_connectie import _osf_aanroep, geef_fouten


class TestOSF_connectie(TestCase):
    @patch('externe_connecties.OSF_connectie._osf_aanroep')
    def test_geef_fouten_als_osf_fouten_teruggeeft(self, mock_osf_aanroep):
        fouten_element_referentie = \
            {'foutcode': 'PF006', 'onderdeel': 'een onderdeel', 'goed': 'een extra info veld: goed'}
        response_referentie = {'fouten': fouten_element_referentie}

        mock_osf_aanroep.return_value = Mock()
        mock_osf_aanroep.return_value.json.return_value = response_referentie

        mock_json_bestand = Mock()

        fouten = geef_fouten(mock_json_bestand)

        self.assertTrue(mock_osf_aanroep.called)
        self.assertEqual(fouten_element_referentie, fouten, 'Het fouten element is niet zoals verwacht.')

    def test_OSF_aanroep_bestand_bestaat_niet(self):
        bestandsnaam = "bestaat_niet.json"

        self.assertRaises(OSFAanroepError, _osf_aanroep, bestandsnaam)
