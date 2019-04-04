from unittest import TestCase, skip

from applicatie.logic.plausibele_berekening import bereken


class TestPlausibeleBerekening(TestCase):
    def test_optellen(self):
        # ARRANGE
        formule = "Totaal_lasten_LR + Totaal_lasten_balans_LR"
        omgeving = {
            'Totaal_lasten_LR': 50,
            'Totaal_lasten_balans_LR': 100
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(150, resultaat)

    def test_aftrekken(self):
        # ARRANGE
        formule = "Totaal_baten_LR - Totaal_lasten_LR"
        omgeving = {
            'Totaal_baten_LR': 50,
            'Totaal_lasten_LR': 100
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(-50, resultaat)

    def test_delen(self):
        # ARRANGE
        formule = "Absoluut_verschil / Totaal_lasten_LR"
        omgeving = {
            'Absoluut_verschil': 50,
            'Totaal_lasten_LR': 100
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(0.5, resultaat)

    def test_absoluut_aftrekken(self):
        # ARRANGE
        formule = "ABS(Emu_saldo_LR - Emu_saldo_FR)"
        omgeving = {
            'Emu_saldo_LR': 50,
            'Emu_saldo_FR': 100
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(50, resultaat)

    @skip
    def test_kleiner_dan(self):
        # ARRANGE
        formule = "(relatief_verschil) <= 0.01"
        omgeving = {
            'Totaal_baten_LR': 50,
            'Totaal_lasten_LR': 100
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(50, resultaat)
