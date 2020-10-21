from unittest import TestCase

from applicatie.logic.codelijst import Codelijst


class TestCodelijst(TestCase):
    def setUp(self) -> None:
        codelijst = [
            {"code": "0.", "omschrijving": "BESTUUR EN ONDERSTEUNING", "subcodes": [
                {"code": "0.1", "omschrijving": "Bestuur"},
                {"code": "0.9", "omschrijving": "Vennootschapsbelasting (VpB)"}]},
            {"code": "1.", "omschrijving": "VEILIGHEID", "subcodes": [
                {"code": "1.1", "omschrijving": "Crisisbeheersing en brandweer"},
                {"code": "1.2", "omschrijving": "Openbare orde en veiligheid"}]},
        ]
        self.codelijst = Codelijst(codelijst)

    def test_geef_terminals(self):
        resultaat = self.codelijst.geef_terminals()
        verwacht = ['0.1', '0.9', '1.1', '1.2']
        self.assertEqual(verwacht, resultaat)

    def test_geef_omschrijving(self):
        resultaat = self.codelijst.geef_omschrijving('0.1')
        verwacht = 'BESTUUR EN ONDERSTEUNING: Bestuur'
        self.assertEqual(verwacht, resultaat)

    def test_geef_parent(self):
        resultaat = self.codelijst.geef_parent('0.1')
        verwacht = '0.'
        self.assertEqual(verwacht, resultaat)
