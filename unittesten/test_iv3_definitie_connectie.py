from unittest import TestCase
from unittest.mock import Mock, patch

from externe_connecties.iv3_definitie_connectie import geef_gebruikersvriendelijke_foutmeldingen


class Test_iv3_definitie_connectie(TestCase):
    @patch('externe_connecties.iv3_definitie_connectie.ophalen_bestand_van_web')
    def test_geef_gebruikersvriendelijke_foutmeldingen_voor_fouten(self, mock_ophalen_bestand_van_web):
        fouten_element_referentie = \
            [{'foutcode': 'PF006',
             'melding': 'een melding met als extra info de velden: <onderdeel> en <goed>.',
             'omschrijving': 'een omschrijving'}]
        inhoud_referentie = {"fouten_overzicht": fouten_element_referentie}

        referentie_resultaat = ["fouttype: plausibiliteitsfout, nummer: 006:"
                                " een melding met als extra info de velden: onderdeel 1 en een extra info veld: goed."]

        mock_ophalen_bestand_van_web.return_value = Mock()
        mock_ophalen_bestand_van_web.return_value = (inhoud_referentie, [])

        fouten_afkomstig_van_osf = [{'foutcode': 'PF006', 'onderdeel': 'onderdeel 1', 'goed': 'een extra info veld: goed'}]

        resultaat = geef_gebruikersvriendelijke_foutmeldingen(fouten_afkomstig_van_osf)

        self.assertTrue(mock_ophalen_bestand_van_web.called)

        self.assertListEqual([], resultaat[1],
                             'Het resultaat van geef_gebruikersvriendelijke_foutmeldingen() is niet zoals verwacht.')
        self.assertEqual(referentie_resultaat, resultaat[0],
                         'Het resultaat van geef_gebruikersvriendelijke_foutmeldingen() is niet zoals verwacht.')
