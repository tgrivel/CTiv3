from unittest import TestCase
from unittest.mock import Mock, patch

from applicatie.main.CustomExceptions import OSFAanroepError
from externe_connecties.OSF_connectie import OSF_aanroep, geef_fouten


class TestOSF_connectie(TestCase):
    @patch('externe_connecties.OSF_connectie.OSF_aanroep')
    def test_geef_fouten_happy_flow(self, mock_OSF_aanroep):
        fouten_element_referentie = \
            {'fout': 123, 'foutcode': 'PF006', 'melding': 'een melding', 'omschrijving': 'een omschrijving'}
        response_referentie = {'fouten': fouten_element_referentie}

        mock_OSF_aanroep.return_value = Mock()
        mock_OSF_aanroep.return_value.json.return_value = response_referentie

        mock_json_bestand = Mock()

        fouten = geef_fouten(mock_json_bestand)

        self.assertTrue(mock_OSF_aanroep.called)
        self.assertEqual(fouten_element_referentie, fouten, 'Het fouten element is niet zoals verwacht.')

    def test_OSF_aanroep_bestand_bestaat_niet(self):
        bestandsnaam = "bestaat_niet.json"

        self.assertRaises(OSFAanroepError, OSF_aanroep, bestandsnaam)
