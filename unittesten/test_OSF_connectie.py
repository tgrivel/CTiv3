from unittest import TestCase
from unittest.mock import Mock, patch

from externe_connecties.OSF_connectie import OSF_aanroep


class TestOSF_connectie(TestCase):
    # @patch('externe_connecties.OSF_connectie.geef_fouten')
    @patch('externe_connecties.OSF_connectie.requests.post')
    def test_stuur_bestand_voor_controle(self, mock_post):
        fouten_element_referentie = \
            {'fouten': {'fout': 123, 'foutcode': 'PF006', 'melding': 'een melding', 'omschrijving': 'een omschrijving'}}
        mock_post.return_value = Mock()
        mock_post.return_value.json.return_value = fouten_element_referentie

        # json_bestand = fake_bestand
        # api_url = mock_server

        # osf_connectie = OSF_connectie()
        # fouten = osf_connectie.stuur_bestand_voor_controle(json_bestand, api_url)
        fouten = OSF_aanroep()

        # self.assertTrue(mc.geef_response.called)
        self.assertEqual(fouten_element_referentie, fouten.json(), 'De lijsten zijn niet gelijk.')
        # self.assertTrue(False)