def maak_codelijst(codelijst):
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
            subcodes = maak_codelijst(item['subcodes'])

            # Voeg parent- en subcode-omschrijving samen
            subcode_update = {subcode: f"{omschrijving}: {subcode_omschrijving}"
                              for (subcode, subcode_omschrijving) in subcodes.items()}
            omschrijvingen.update(subcode_update)

    return omschrijvingen
