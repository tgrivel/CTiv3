from jsonschema import Draft4Validator
import logging


_logger = logging.getLogger(__file__)


def controle_met_schema(json_bestand, json_schema):
    foutmeldingen = []
    v = Draft4Validator(json_schema)
    errors = sorted(v.iter_errors(instance=json_bestand), key=lambda e: e.path)

    numerr = 0
    for n, error in enumerate(errors):
        if len(error.context) == 0:
            numerr = numerr + 1
        else:
            numerr = numerr + len(error.context)

        foutmelding = []
        foutmelding.append("Fout #{}:".format(n + 1))
        foutmelding.append(", ".join(list(error.schema_path)))
        foutmelding.append(": " + error.message)
        foutmeldingen.append(" ".join(foutmelding))

        suberrors = sorted(error.context, key=lambda e: e.schema_path)
        for m, suberror in enumerate(suberrors):
            foutmelding = []
            foutmelding.append("Fout #{}:".format(n + 1))
            foutmelding.append(", ".join(str(x) for x in list(suberror.schema_path)))
            foutmelding.append(": " + suberror.message)
            foutmeldingen.append(" ".join(foutmelding))

    foutmeldingen.append("Totaal aantal fouten op basis van schema controle: {}".format(numerr))
    return foutmeldingen
