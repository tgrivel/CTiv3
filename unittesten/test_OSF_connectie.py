from unittest import TestCase
from unittest.mock import Mock, patch

from externe_connecties.OSF_connectie import OSF_connectie


class TestOSF_connectie(TestCase):
    @patch('externe_connecties.OSF_connectie.requests.post')
    def test_stuur_bestand_voor_controle(self, mock_post):
        fouten_element_referentie = \
        {'fouten': {'fout': 11333.0,
                    'foutcode': 'PF006',
                    'goed': 50,
                    'melding': 'Totaal lasten taakvelden is niet gelijk aan totaal baten '
                               'taakvelden. Het gevonden verschil is 24571.0, terwijl 50 '
                               'maximaal is toegestaan.',
                    'omschrijving': 'Controle 6 onvoldoende'}}
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = fouten_element_referentie

        # json_bestand = fake_bestand
        # api_url = mock_server

        osf_connectie = OSF_connectie()
        # fouten = osf_connectie.stuur_bestand_voor_controle(json_bestand, api_url)
        fouten = osf_connectie.geef_fouten()

        self.assertEqual(fouten_element_referentie, fouten, 'De lijsten zijn niet gelijk.')
        # self.assertTrue(False)