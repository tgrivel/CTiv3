from unittest import TestCase

from applicatie.logic.foutmeldingen import geef_gebruikersvriendelijke_foutmeldingen


class TestFoutmeldingen(TestCase):
    def test_geef_gebruikersvriendelijke_foutmeldingen_voor_fouten(self):
        fouten_overzicht_voorbeeld = \
            [{'foutcode': 'PF006',
             'melding': 'een melding met als extra info de velden: <onderdeel> en <goed>.',
             'omschrijving': 'een omschrijving'}]

        referentie_resultaat = ["fouttype: plausibiliteitsfout, nummer: 006:"
                                " een melding met als extra info de velden: onderdeel 1 en een extra info veld: goed."]

        fouten_afkomstig_van_osf = [{'foutcode': 'PF006', 'onderdeel': 'onderdeel 1', 'goed': 'een extra info veld: goed'}]

        resultaat = geef_gebruikersvriendelijke_foutmeldingen(fouten_afkomstig_van_osf, fouten_overzicht_voorbeeld)

        self.assertEqual(referentie_resultaat, resultaat,
                         'Het resultaat van geef_gebruikersvriendelijke_foutmeldingen() is niet zoals verwacht.')
