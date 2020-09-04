class GrijzeCel(object):
    def __init__(self, grijze_cellen):
        self._taakvelden = _maak_taakvelden_tabel(grijze_cellen)
        #TODO self._balanscodes = _maak_balanscode_tabel(grijze_cellen) TODO
        # self._hierarchie = _maak_hierarchie(grijze_cellen)

    def geef_taakveld(self, categorie):
        """Geef het taakveld bij een categorie."""
        return self._taakvelden.get(categorie) or ''


def _maak_taakvelden_tabel(grijze_cellen):
    """Maak een mapping van categorie naar een taakveld."""

    taakvelden = {}
    for item in grijze_cellen:
        categorie = item['categorie']

        taakveld = item.get('taakveld') or ''
        taakvelden[categorie] = taakveld

    return taakvelden


def _maak_hierarchie(grijze_cellen):
    """Maak een mapping van childcode naar parentcode."""
    hierarchie = {}

    for item in grijze_cellen:
        code = item['code']

        if 'subcodes' in item:
            for subitem in item['subcodes']:
                subcode = subitem['code']
                hierarchie[subcode] = code

            # Recursie
            hierarchie.update(_maak_hierarchie(item['subcodes']))

    return hierarchie
