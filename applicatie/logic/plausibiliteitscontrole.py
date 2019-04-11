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

        resultaat = ControleResultaat(self)

        for stap in self.definitie:
            variabele = stap['variabele']
            expressie = stap['expressie']
            omschrijving = stap['omschrijving']

            if "check" in expressie:
                formule = expressie['formule'] + ' ' + expressie['check']

                try:
                    controle_resultaat = bool(bereken(formule, omgeving))
                except RekenFout as e:
                    resultaat.toevoegen_opmerking(e.melding, omschrijving, is_fout=True)
                    break
                else:
                    if controle_resultaat:
                        resultaat.toevoegen_opmerking(f'Controle {formule} is waar.', omschrijving)
                    else:
                        resultaat.toevoegen_opmerking(f'Controle {formule} is onwaar.', omschrijving, is_fout=True)

            elif "formule" in expressie:
                try:
                    uitkomst = bereken(expressie['formule'], omgeving)
                except RekenFout as e:
                    melding = f"Kan `{variabele}' niet berekenen: {e.melding}."
                    resultaat.toevoegen_opmerking(melding, omschrijving, is_fout=True)
                    break
                else:
                    omgeving[variabele] = uitkomst
                    resultaat.toevoegen_opmerking(f"{variabele} = {uitkomst}", omschrijving)
            else:
                query = expressie
                rekeningkant = query.pop('rekeningsoort')
                rekening_data = data[rekeningkant]
                matches = [rij for rij in rekening_data
                           if all(rij[key] == query[key] for key in query)]

                if not matches:
                    melding = (f"Kan variabele `{variabele}' niet ophalen: "
                               f"Er is geen record met eigenschappen {dict(query)}.")
                    resultaat.toevoegen_opmerking(melding, omschrijving, is_fout=True)
                    break

                totaal_bedrag = sum(match['bedrag'] for match in matches)
                omgeving[variabele] = totaal_bedrag
                rapportage.append(f"{variabele} = {totaal_bedrag}")
                resultaat.toevoegen_opmerking(f"{variabele} = {totaal_bedrag}", omschrijving)

        return resultaat


class ControleResultaat(object):
    def __init__(self, controle):
        self.controle = controle
        self.is_geslaagd = True  # Tot tegendeel bewezen is
        self._rapportage = []

    def toevoegen_opmerking(self, opmerking, omschrijving="", is_fout=False):
        """Voeg een opmerking toe.

        Opmerking bevat extra informatie over de uit te voeren controle.
        is_fout vermeld of de opmerking inhoud dat de controle gefaald is.
        """
        self._rapportage.append((opmerking, omschrijving))

        if is_fout:
            self.is_geslaagd = False

    def rapportage(self):
        """Uitgebreide rapportage om de tussenstappen van de contole te printen."""
        return self._rapportage
