from unittest import TestCase

from applicatie.logic.grijze_cel import GrijzeCel


class TestGrijzeCel(TestCase):
    def setUp(self) -> None:
        lasten = [
            {"categorie": "3.1", "taakveld": "0.1"},
            {"categorie": "3.4.1", "taakveld": "0.2"},
            {"categorie": "4.1.1", "taakveld": "0.3"},
            {"categorie": "4.4.3", "taakveld": "0.4"},
            {"categorie": "4.4.4", "taakveld": "0.5"}]
        self.grijze_cellen = GrijzeCel(lasten)


    def test_geef_taakveld(self):
        categorie = '3.1';
        taakveld = self.grijze_cellen.geef_taakveld(categorie)
        verwacht_taakveld = '0.1'
        self.assertEqual(verwacht_taakveld, taakveld)
