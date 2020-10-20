from applicatie.logic.inlezen import ophalen_bestand_van_web
from config.configurations import IV3_REPO_PATH
import logging


_logger = logging.getLogger(__file__)


def geef_gebruikersvriendelijke_foutmeldingen(fouten):
    """
    Haal gebruikers vriendelijke vertalingen uit fouten.json voor fouten.
    """
    inhoud, foutmeldingen = ophalen_bestand_van_web(IV3_REPO_PATH, 'fouten.json', 'foutenbestand')
    if foutmeldingen:
        return foutmeldingen

    fouten_overzicht = inhoud.get("fouten_overzicht")

    for fout in fouten:
        if type(fout) == str:
            # Als de fout een string is wordt deze gewoon getoond.
            foutmeldingen.append(fout)
            continue
        # Als fout een dict is komt hij van OSF controle en moet hij enkele bewerkingen ondergaan voor we hem tonen:
        fout_gevonden = False
        fout_uit_controle = fout.get("foutcode")
        # vind juiste fouten-info uit fouten.json.
        for referentie_fout in fouten_overzicht:
            referentie_foutcode = referentie_fout.get("foutcode")
            if referentie_foutcode == fout_uit_controle:
                fout_gevonden = True

                # omschrijving = referentie_fout.get("omschrijving")
                melding = referentie_fout.get("melding")
                melding_met_extra_info = _voeg_extra_info_toe(melding, fout)

                foutmeldingen.append("fouttype: " + _vertaal_foutcode_in_fouttype(referentie_foutcode) +
                                           ", nummer: " + _vertaal_foutcode_in_foutnummer(referentie_foutcode) +
                                           ": " + melding_met_extra_info)
                break
        if not fout_gevonden:
            _logger.info(
                "Er is een foutcode teruggegeven door de OSF API die niet voorkomt in het fouten.json bestand.")
            foutmeldingen.append("Er zit een onbekende fout in het bestand,"
                                       " contacteer alstublieft het team Overheidsfinancien.")
    return foutmeldingen


def _vertaal_foutcode_in_fouttype(foutcode):
    fouttypes = {"SF": "schemafout", "DF": "definitiefout", "PF": "plausibiliteitsfout"}
    return fouttypes.get(foutcode[:2])


def _vertaal_foutcode_in_foutnummer(foutcode):
    return foutcode[2:]


def _voeg_extra_info_toe(melding, fout_boodschap):
    """
    Haal extra info uit de fout_boodschap komende van OSF, en voeg deze toe aan de melding.
    De extra info kan zijn: <fout>, <goed>, <extra>, <onderdeel>.
    """
    fout = fout_boodschap.get("fout")
    goed = fout_boodschap.get("goed")
    extra = fout_boodschap.get("extra")
    onderdeel = fout_boodschap.get("onderdeel")
    extra_info = {"<fout>": fout, "<goed>": goed, "<extra>": extra, "<onderdeel>": onderdeel}
    for key, value in extra_info.items():
        if value != None:
            # vind plek in melding om extra info in te vullen.
            index = melding.find(key)
            if index != -1:
                # vul in melding de extra info in.
                melding_lijst = melding.split(key)

                melding_lijst.insert(1, str(value))
                melding = "".join(melding_lijst)
    return melding
