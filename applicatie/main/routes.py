import io
import json
import sys
import logging

from flask import render_template, request, current_app

from applicatie.main.custom_exceptions import OSFAanroepError
from applicatie.main import bp
from applicatie.main.verwerking import Verwerking
from config.configurations import EXTERNE_CONTROLE, VERSIE
from applicatie.logic.foutmeldingen import geef_gebruikersvriendelijke_foutmeldingen


_logger = logging.getLogger(__file__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    """
    Hoofdpagina. We controleren het type van de browser en of er een bestand is geselecteerd.
    Ook is hier de logica ondergebracht voor het verwerken van een mutatie zodat deze zichtbaar wordt
    door het verversen van het scherm.
    """

    # javascript debug status
    js_debug_status = (current_app.config['ENV'] == 'debugjavascript')

    if request.method == 'POST':
        reqform = request.form.to_dict()
        if (not request.files.get('file')) and 'data' in reqform:
            # Mutatie verwerken
            mutatie = reqform

            data = json.loads(mutatie.pop('data'))
            bestandsnaam = mutatie.pop('bestandsnaam')
            uploaded_file = io.BytesIO(json.dumps(data).encode('utf-8'))
            return matrix(uploaded_file, mutatie)

        elif not request.files.get('file'):
            foutmeldingen = ['Geen json bestand geselecteerd']
            return geef_index_met_foutmeldingen(foutmeldingen, js_debug_status)

        else:
            browsertype = request.user_agent.browser
            if browsertype not in ['firefox', 'chrome']:
                foutmeldingen = ['Deze website werkt alleen met Firefox en Chrome browsers']
                return geef_index_met_foutmeldingen(foutmeldingen, js_debug_status)
            uploaded_file = request.files['file']
            bestandsnaam = uploaded_file.filename

            if EXTERNE_CONTROLE and bestandsnaam != '':
                uploaded_file.save(bestandsnaam)

            return matrix(uploaded_file)

    elif request.method == 'GET':
        foutmeldingen = []
        browsertype = request.user_agent.browser
        if browsertype not in ['firefox', 'chrome']:
            foutmeldingen = ['Deze website werkt alleen met Firefox en Chrome browsers']
        return geef_index_met_foutmeldingen(foutmeldingen, js_debug_status)


def geef_tabnaam(waarde_kant):
    """
    Automatisch open bijbehorende tab.
    """
    if waarde_kant == 'lasten':
        tabnaam = 'LastenLR'
    elif waarde_kant == 'baten':
        tabnaam = 'BatenLR'
    elif waarde_kant == 'balans_lasten':
        tabnaam = 'LastenBM'
    elif waarde_kant == 'balans_baten':
        tabnaam = 'BatenBM'
    elif waarde_kant == 'balans_standen':
        tabnaam = 'Balans'
    elif waarde_kant == 'kengetallen':
        tabnaam = 'Kengetallen'
    elif waarde_kant == 'beleidsindicatoren':
        tabnaam = 'Beleidsindicatoren'
    elif waarde_kant == 'bulkcorrecties':
        tabnaam = 'Bulk_correcties'
    else:
        # Foutafhandeling
        print('Fout: Onbekende waarde_kant', waarde_kant)
        tabnaam = None
    return tabnaam


# opmerking: we staan alleen de POST-methode toe, anders krijg je een fout.
@bp.route("/matrix", methods=['POST'])
def matrix(jsonbestand, mutatie=None):
    """
    Haal het JSON-bestand op en geef evt. foutmeldingen terug.
    Indien geen fouten, laad de pagina met een overzicht van de data.
    """
    # javascript debug status
    js_debug_status = (current_app.config['ENV'] == 'debugjavascript')

    try:
        verwerking = Verwerking(jsonbestand)
    except OSFAanroepError:
        foutmeldingen = ['Er is een fout opgetreden bij de controle van het bestand,'
                         ' probeert u het opnieuw of contacteer team Overheidsfinancien.']
        return geef_index_met_foutmeldingen(foutmeldingen, js_debug_status)

    foutmeldingen = []
    if verwerking.controle_fouten:
        # Fouten geconstateerd door OSF.
        foutmeldingen = geef_gebruikersvriendelijke_foutmeldingen(verwerking.controle_fouten,
                                                                  verwerking.fouten_overzicht)
    if verwerking.fouten:
        # Fouten geconstateerd door onszelf toevoegen.
        foutmeldingen.extend(verwerking.fouten)
    if foutmeldingen:
        return geef_index_met_foutmeldingen(foutmeldingen, js_debug_status)

    if mutatie and not verwerking.fouten:
        waarde_kant = mutatie.pop('waarde_kant')
        tabnaam = geef_tabnaam(waarde_kant)

        if not waarde_kant == 'bulkcorrecties':
            # verwerken van een enkele correctie
            try:
                if '.' in mutatie['bedrag']:
                    bedrag = float(mutatie['bedrag'])
                else:
                    bedrag = int(mutatie['bedrag'])
            except ValueError:
                print(f"Fout: bedrag is geen numerieke waarde {mutatie['bedrag']})", file=sys.stderr)
                bedrag = 0

            mutatie['bedrag'] = bedrag
            # omschrijving toevoegen aan het 'details' element
            mutatie['details'] = {"omschrijving": "Mutatie toegevoegd met Ocido."}
            verwerking.muteer(waarde_kant, mutatie)

        else:
            # verwerken van bulkcorrecties
            bulkcorrecties = json.loads(mutatie['bulkcorrecties'])
            for correctie in bulkcorrecties.values():
                for key, corr in correctie.items():
                    verwerking.muteer(key, corr)

    else:
        tabnaam = None

    verwerking.run()

    if verwerking.fouten:
        return geef_index_met_foutmeldingen(verwerking.fouten, js_debug_status)

    # Render sjabloon
    params = {
        'bestandsnaam': jsonbestand.filename,
        'tabnaam': tabnaam,
        'data': verwerking.data_bestand,
        'sjabloon': verwerking.sjabloon_meta,
        'draaitabellen': verwerking.draaitabellen,
        'controle_resultaten': verwerking.controle_resultaten,
        'meta': verwerking.metadata,
        'contact': verwerking.contact,
        'debug_status': js_debug_status,

        # hebben we onderstaande nog nodig?
        'errormessage': "",
    }

    return render_template("matrix.html", **params)


def geef_index_met_foutmeldingen(foutmeldingen, js_debug_status):
    return render_template("index.html", errormessages=foutmeldingen, debug_status=js_debug_status, versienummer=VERSIE)
