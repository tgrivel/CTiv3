from unittest import TestCase
from unittest.mock import Mock, patch

from externe_connecties.OSF_connectie import OSF_aanroep, geef_fouten


class TestOSF_connectie(TestCase):
    @patch('externe_connecties.OSF_connectie.OSF_aanroep')
    # @patch('externe_connecties.OSF_connectie.requests.post')
    def test_stuur_bestand_voor_controle(self, mock_OSF_aanroep):
        fouten_element_referentie = \
            {'fout': 123, 'foutcode': 'PF006', 'melding': 'een melding', 'omschrijving': 'een omschrijving'}
        response_referentie = {'fouten': fouten_element_referentie}

        mock_OSF_aanroep.return_value = Mock()
        mock_OSF_aanroep.return_value.json.return_value = response_referentie

        # json_bestand = fake_bestand
        # api_url = mock_server

        # osf_connectie = OSF_connectie()
        # fouten = osf_connectie.stuur_bestand_voor_controle(json_bestand, api_url)
        fouten = geef_fouten()

        self.assertTrue(mock_OSF_aanroep.called)
        self.assertEqual(fouten_element_referentie, fouten, 'Het fouten element is niet zoals verwacht.')
