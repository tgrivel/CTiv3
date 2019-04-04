import operator

from applicatie.logic.plausibele_berekening import bereken


gelijkheidsoperatoren = {
    '>': operator.gt,
    '<': operator.lt,
    '=': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
}


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
                # check = expressie['check']

                # operator_functie = None
                # rechterkant = None
                # for operator in gelijkheidsoperatoren:
                #     if check.startswith(operator):
                #         operator_functie = gelijkheidsoperatoren[operator]
                #         rechterkant = check[:len(operator)]

                # if operator_functie and rechterkant:
                #     rapportage.append("Kan niet rekenen met")

                # resultaat_links = bereken(expressie['formule'])
                # resultaat_rechts = bereken(rechterkant)

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
