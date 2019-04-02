from applicatie.logic.plausibele_berekening import bereken


class PlausibiliteitsControle(object):
    def __init__(self, omschrijving, definitie):
        self.omschrijving = omschrijving
        self.definitie = definitie

    def run(self, data) -> "ControleResultaat":
        """Voer de controles uit en retourneer een ControleResultaat."""

        omgeving = dict()
        rapportage = []

        for stap in self.definitie:
            variabele = stap['variabele']
            expressie = stap['expressie']

            if "check" in expressie:
                formule = expressie['formule'] + ' ' + expressie['check']
                controle_resultaat = bool(bereken(formule, omgeving))

                if controle_resultaat:
                    rapportage.append(f'Controle {formule} is waar')
                else:
                    rapportage.append(f'Controle {formule} is onwaar')

            if "formule" in expressie:
                formule = bereken(expressie['formule'], omgeving)
                omgeving[variabele] = formule
                rapportage.append(f"{variabele} = {totaal_bedrag}")
            else:
                query = expressie
                rekeningkant = query.pop('rekeningsoort')
                rekening_data = data[rekeningkant]
                matches = [rij for rij in rekening_data
                           if all(rij[key] == query[key] for key in query)]

                if not matches:
                    rapportage.append(f'Er is geen record met eigenschappen {query}!')

                totaal_bedrag = sum(match['bedrag'] for match in matches)
                omgeving[variabele] = totaal_bedrag
                rapportage.append(f"{variabele} = {totaal_bedrag}")

        return ControleResultaat(self, omgeving, rapportage)


class ControleResultaat(object):
    def __init__(self, controle, omgeving, rapportage):
        self.controle = controle
        self.omgeving = omgeving
        self._rapportage = rapportage

    def is_geslaagd(self):
        """Retoerneer of de controle geslaagd is."""
        # return True
        return False

    def rapportage(self):
        """Uitgebreide rapportage om de tussenstappen van de contole te printen."""
        return self._rapportage
        # return [
        #     "a = 6",
        #     "b = 4",
        #     "De check is gefaald. Er moet gelden a > b, maar a = 6 en b = 4"
        # ]
