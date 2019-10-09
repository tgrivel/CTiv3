class Codelijst(object):
    def __init__(self, codelijst):
        self._omschrijvingen = _maak_omschrijving_tabel(codelijst)
        self._hierarchie = _maak_hierarchie(codelijst)

    def geef_parent(self, code):
        """Geef de parentcode bij een code"""
        return self._hierarchie[code]

    def geef_omschrijving(self, code):
        """Geef de omschrijving bij een code."""
        return self._omschrijvingen.get(code) or ''

    def geef_terminals(self):
        """Geef de codes terug die geen subcodes hebben."""

        terminals = []
        for code in self._omschrijvingen.keys():
            if code not in self._hierarchie.values():
                terminals.append(code)

        return terminals


def _maak_omschrijving_tabel(codelijst):
    """Gegeven een codelijst maak een mapping van code naar een omschrijving.

    Bij geneste codelijsten, wordt een dubbele punt tussen de parent- en childomschrijving geplaatst.
    """

    omschrijvingen = {}
    for item in codelijst:
        code = item['code']

        # TODO Gebruik omschrijving en verwijder oude naam description uit definitiebestanden
        omschrijving = item.get('omschrijving') or item.get('description') or ''
        omschrijvingen[code] = omschrijving

        if 'subcodes' in item:
            subcodes = _maak_omschrijving_tabel(item['subcodes'])

            # Voeg parent- en subcode-omschrijving samen
            subcode_update = {subcode: f"{omschrijving}: {subcode_omschrijving}"
                              for (subcode, subcode_omschrijving) in subcodes.items()}
            omschrijvingen.update(subcode_update)

    return omschrijvingen


def _maak_hierarchie(codelijst):
    """Maak een mapping can childcode naar parentcode."""
    hierarchie = {}

    for item in codelijst:
        code = item['code']

        if 'subcodes' in item:
            for subitem in item['subcodes']:
                subcode = subitem['code']
                hierarchie[subcode] = code

            # Recursie
            hierarchie.update(_maak_hierarchie(item['subcodes']))

    return hierarchie
