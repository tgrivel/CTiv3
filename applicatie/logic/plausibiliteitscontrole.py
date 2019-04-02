class PlausibiliteitsControle(object):
    def __init__(self, omschrijving, definitie):
        self.omschrijving = omschrijving
        self.definitie = definitie

    def run(self) -> "ControleResultaat":
        # Voer de controles uit en retourneer een ControleResultaat
        return ControleResultaat(self)


class ControleResultaat(object):
    def __init__(self, controle):
        self.controle = controle

    def is_geslaagd(self):
        # Of de controle geslaagd is of niet
        # return True
        return False

    def rapportage(self):
        # Uitgebreide rapportage om de tussenstappen van de contole te printen
        return [
            "a = 6",
            "b = 4",
            "De check is gefaald. Er moet gelden a > b, maar a = 6 en b = 4"
        ]
