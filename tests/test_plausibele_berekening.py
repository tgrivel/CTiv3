from unittest import TestCase

from applicatie.ongebruikt.plausibele_berekening import bereken


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

    def test_delen2(self):
        # ARRANGE
        formule = "(Absoluut_verschil / Totaal_lasten_LR)"
        omgeving = {
            'Absoluut_verschil': 38254,
            'Totaal_lasten_LR': 4801
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertAlmostEqual(7.967923349302229, resultaat)

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

    def test_absoluut_aftrekken2(self):
        # ARRANGE
        formule = "ABS(Emu_saldo_LR - Emu_saldo_FR)"
        omgeving = {
            'Emu_saldo_LR': 546,
            'Emu_saldo_FR': 0
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(546, resultaat)

    def test_kleiner_dan(self):
        # ARRANGE
        formule = "(relatief_verschil) <= 0.01"
        omgeving = {
            'relatief_verschil': 50,
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(False, resultaat)

    def test_complexe_expressie(self):
        # ARRANGE
        formule = "alpha * alpha + beta * beta"
        omgeving = {
            'alpha': 3,
            'beta': 4,
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(25, resultaat)

    def test_complexe_expressie2(self):
        # ARRANGE
        formule = "alpha * (alpha + beta) * beta"
        omgeving = {
            'alpha': 3,
            'beta': 4,
        }

        # ACT
        resultaat = bereken(formule, omgeving)
        self.assertEqual(84, resultaat)
