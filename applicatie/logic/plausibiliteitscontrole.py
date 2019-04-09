import operator

from applicatie.logic.plausibele_berekening import bereken, RekenFout

class PlausibiliteitsControle(object):
    def __init__(self, omschrijving, definitie):
        self.omschrijving = omschrijving
        self.definitie = definitie

    def run(self, data) -> "ControleResultaat":
        """Voer de controles uit en retourneer een ControleResultaat."""

        omgeving = dict()
        rapportage = []

        is_geslaagd = True  # Tot tegendeel bewezen is

        for stap in self.definitie:
            variabele = stap['variabele']
            expressie = stap['expressie']

            if "check" in expressie:
                formule = expressie['formule'] + ' ' + expressie['check']

                try:
                    controle_resultaat = bool(bereken(formule, omgeving))
                except RekenFout as e:
                    rapportage.append(e.melding)
                    is_geslaagd = False
                    break
                else:
                    if controle_resultaat:
                        rapportage.append(f'Controle {formule} is waar')
                    else:
                        rapportage.append(f'Controle {formule} is onwaar')

            if "formule" in expressie:
                try:
                    uitkomst = bereken(expressie['formule'], omgeving)
                except RekenFout as e:
                    melding = f"Kan `{variabele}' niet berekenen: {e.melding}"
                    rapportage.append(melding)
                    is_geslaagd = False
                    break
                else:
                    omgeving[variabele] = uitkomst
                    rapportage.append(f"{variabele} = {uitkomst}")
            else:
                query = expressie
                rekeningkant = query.pop('rekeningsoort')
                rekening_data = data[rekeningkant]
                matches = [rij for rij in rekening_data
                           if all(rij[key] == query[key] for key in query)]

                if not matches:
                    melding = (f"Kan variabele `{variabele}' niet ophalen: "
                               f"Er is geen record met eigenschappen {dict(query)}!)")
                    rapportage.append(melding)

                totaal_bedrag = sum(match['bedrag'] for match in matches)
                omgeving[variabele] = totaal_bedrag
                rapportage.append(f"{variabele} = {totaal_bedrag}")

        return ControleResultaat(self, omgeving, is_geslaagd, rapportage)


class ControleResultaat(object):
    def __init__(self, controle, omgeving, is_geslaagd, rapportage):
        self.controle = controle
        self.omgeving = omgeving
        self._is_geslaagd = is_geslaagd
        self._rapportage = rapportage

    def is_geslaagd(self):
        """Retoerneer of de controle geslaagd is."""
        return self._is_geslaagd

    def rapportage(self):
        """Uitgebreide rapportage om de tussenstappen van de contole te printen."""
        return self._rapportage
        # return [
        #     "a = 6",
        #     "b = 4",
        #     "De check is gefaald. Er moet gelden a > b, maar a = 6 en b = 4"
        # ]
