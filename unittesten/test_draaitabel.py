from unittest import TestCase

from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.codelijst import Codelijst


class TestDraaiTabel(TestCase):
    def setUp(self) -> None:
        self.rij_naam = "taakveld"
        self.kolom_naam ="categorie"
        self.grijze_cellen = [
                {self.kolom_naam:"2.1", self.rij_naam:"0.1"},
			    {self.kolom_naam:"3.1", self.rij_naam:"0.1"},
			    {self.kolom_naam:"3.4.1", self.rij_naam:"0.1"}]
        self.draai_tabel = DraaiTabel(
            naam='lasten',
            data=[],
            rij_naam=self.rij_naam,
            kolom_naam=self.kolom_naam,
            rij_codelijst=Codelijst(codelijst=[{"code": "0", "omschrijving": "onzin"}]),
            kolom_codelijst=Codelijst(codelijst=[{"code": "0", "omschrijving": "onzin"}]),
            grijze_cellen=self.grijze_cellen)

    def test_is_grijze_cel_voor_niet_bestaande_cel(self):
        rij = "rij_bestaat_niet"
        kolom = "kolom_bestaat_niet"

        resultaat = self.draai_tabel.is_grijze_cel(rij, kolom)
        self.assertFalse(resultaat, "De cel van de tabel bestaat niet en kan dus ook niet grijs zijn.")

    def test_is_grijze_cel_voor_witte_cel(self):
        rij = "0.2"
        kolom = "8.1"

        resultaat = self.draai_tabel.is_grijze_cel(rij, kolom)
        self.assertFalse(resultaat, "De cel van de tabel zou een witte cel moeten zijn, maar is dat niet.")

    def test_is_grijze_cel_voor_grijze_cellen(self):
        for grijze_cel in self.grijze_cellen:
            rij = grijze_cel[self.rij_naam]
            kolom = grijze_cel[self.kolom_naam]

            resultaat = self.draai_tabel.is_grijze_cel(rij, kolom)
            self.assertTrue(resultaat, "De cel van de tabel zou een grijze cel moeten zijn, maar is dat niet.")
