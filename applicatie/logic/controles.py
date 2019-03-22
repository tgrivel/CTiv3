from jsonschema import Draft4Validator
import logging


_logger = logging.getLogger(__file__)


def controle_met_schema(json_bestand, json_schema):
    """"Controleer een json data bestand
    aan de hand van een json schema.
    We gebruiken hierbij het jsonschema package
    zie https://pypi.org/project/jsonschema/ """
    foutmeldingen = []
    v = Draft4Validator(json_schema)
    errors = sorted(v.iter_errors(instance=json_bestand), key=lambda e: e.path)

    numerr = 0  # tel het aantal unieke fouten
    for n, error in enumerate(errors):
        if len(error.context) == 0:
            numerr = numerr + 1
        else:
            numerr = numerr + len(error.context)

        fout = list()
        fout.append("Fout #{}:".format(n + 1))
        fout.append(", ".join(list(error.schema_path)))
        fout.append(": " + error.message)
        foutmeldingen.append(" ".join(fout))

        suberrors = sorted(error.context, key=lambda e: e.schema_path)
        for m, suberror in enumerate(suberrors):
            fout = list()
            fout.append("Subfout #{}.{}:".format(n + 1, m + 1))
            fout.append(", ".join(str(x) for x in list(suberror.schema_path)))
            fout.append(": " + suberror.message)
            foutmeldingen.append(" ".join(fout))

    if numerr > 0:
        foutmeldingen.append(
            "Samenvatting: totaal {} unieke fouten gevonden op basis van schema controle.".format(numerr))
        _logger.info("Fouten gevonden op basis van schema controle")
    return foutmeldingen


def extract_values_from_json(obj: object, key: str, key2: str, detail: bool):
    """Pull all values of specified key from nested JSON."""
    arr = []
    parent = ''
    level = 0

    def extract(obj: object, arr: list, key: str, key2: str, level: int, parent: str, detail: bool):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key, key2, level, parent, detail)
                elif k == key:
                    level = level + 1
                    val_k2 = ''
                    for k2, v2 in obj.items():
                        if k2 == key2:
                            val_k2 = v2
                    arr.append(v)
                    if detail:
                        arr.append(val_k2)
                        arr.append(level)
                        arr.append(parent)
                    parent = v
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key, key2, level, parent, detail)
        return arr

    results = extract(obj, arr, key, key2, level, parent, detail)
    return results


def controle_met_defbestand(json_bestand, json_definities):
    """"Controleer een json data bestand
    aan de hand van de codelijsten in het definitiebestand"""

    codefouten = []

    # codelijsten ophalen uit definitiebestand
    cl = json_definities['codelijsten']

    # maak per codelijst-item een lijst van de voorkomende codes
    # hierbij gebruiken we een hulpfunctie extract_values_from_json
    codechecklijst = {}
    for k in list(cl.keys()):
        codechecklijst.update({k: extract_values_from_json(cl[k], 'code', 'description', True)})

    foutstring = "Codefout in [data]:[{}] record #{}: {} {} komt niet voor in de codelijst voor '{}'"

    # loop per rekening door de data
    for rekening, data in json_bestand['data'].items():
        for pos, records in enumerate(data):
            for key, val in records.items():
                cl_key = key

                # we gebruiken codelijst 'standper' tijdelijk niet
                # ivm inconsistentie tussen schema en codelijst
                if cl_key == 'standper':
                    continue

                # voor categorie hebben we twee codelijsten
                # afhankelijk van rekening
                if cl_key == 'categorie':
                    if 'lasten' in rekening:
                        cl_key += '_lasten'
                    if 'baten' in rekening:
                        cl_key += '_baten'

                # indien een codelijst beschikbaar is voor de sleutel,
                # checken of de waarde hierin voorkomt
                if cl_key in list(cl.keys()):
                    if val not in codechecklijst.get(cl_key)[0::4]:
                        codefouten.append(foutstring.format(rekening, pos, key, val, cl_key))

    if codefouten:
        codefouten.append(
            "Samenvatting: totaal {} fouten gevonden op basis van codelijst controle.".format(len(codefouten)))
        _logger.info("Fouten gevonden op basis van codelijst controle met def bestand")
    return codefouten
