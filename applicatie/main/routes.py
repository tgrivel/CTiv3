import io
import json
import sys

from flask import render_template, request

from applicatie.logic.aggregeren import aggregeren_volledig
from applicatie.logic.codelijst import Codelijst
from applicatie.logic.controles import controle_met_defbestand
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand, ophalen_bestand_van_web
from applicatie.logic.plausibiliteitscontrole import PlausibiliteitsControle
from applicatie.main import bp
from config.configurations import IV3_REPO_PATH, IV3_DEF_FILE


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        # Mutatie verwerken
        mutatie = dict(request.form)
        data = json.loads(mutatie.pop('data'))

        waarde_kant = mutatie.pop('waarde_kant')
        bestandsnaam = mutatie.pop('bestandsnaam')

        # Automatisch open bijbehorende tab
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
        else:
            # Foutafhandeling
            print('Fout: Onbekende waarde_kant', waarde_kant, file=sys.stderr)
            tabnaam = None

        try:
            if '.' in mutatie['bedrag']:
                bedrag = float(mutatie['bedrag'])
            else:
                bedrag = int(mutatie['bedrag'])
        except ValueError:
            print(f"Fout: bedrag is geen numerieke waarde {mutatie['bedrag']})", file=sys.stderr)
            bedrag = 0

        mutatie['bedrag'] = bedrag
        mutatie['opmerking'] = "Mutatie toegevoegd met CTiv3."

        data['data'][waarde_kant].append(mutatie)
        jsonbestand = io.BytesIO(json.dumps(data).encode('utf-8'))
        return matrix(jsonbestand, bestandsnaam, tabnaam)

    elif request.method == 'POST':
        if not request.files.get('file', None):
            return render_template("index.html", errormessages=['Geen json bestand geselecteerd'])
        else:
            browsertype = request.user_agent.browser
            if browsertype not in ['firefox', 'chrome']:
                fouten = ['Deze website werkt alleen met Firefox en Chrome browsers']
                return render_template("index.html", errormessages=fouten)
            jsonfile = request.files['file']
            jsonfilename = jsonfile.filename
            return matrix(jsonbestand=jsonfile, jsonbestandsnaam=jsonfilename)
    elif request.method == 'GET':
        fouten = []
        browsertype = request.user_agent.browser
        if browsertype not in ['firefox', 'chrome']:
            fouten = ['Deze website werkt alleen met Firefox en Chrome browsers']
        return render_template("index.html", errormessages=fouten)


@bp.route("/matrix", methods=['GET', 'POST'])
def matrix(jsonbestand, jsonbestandsnaam, tabnaam=None):
    """ Haal het JSON-bestand op en geef evt. foutmeldingen terug
    Indien geen fouten, laad de pagina met een overzicht van de data.
    """

    if jsonbestand:
        # json data bestand ophalen en evt. fouten teruggeven
        data_bestand, fouten = ophalen_en_controleren_databestand(jsonbestand)

        # json definitie bestand ophalen van web
        # in de controles bij het inlezen is al bepaald dat dit bestaat
        if not fouten:
            meta = data_bestand['metadata']
            overheidslaag = meta['overheidslaag']
            boekjaar = meta['boekjaar']
            bestandsnaam = IV3_DEF_FILE.format(overheidslaag, boekjaar)
            definitie_bestand, fouten = ophalen_bestand_van_web(IV3_REPO_PATH, bestandsnaam, 'definitiebestand')

        if not fouten:
            # Controle databestand met definitiebestand
            fouten = controle_met_defbestand(data_bestand, definitie_bestand)

        if not fouten:
            # json bestand is opgehaald en geen fouten zijn gevonden
            # vervolgens data aggregeren en tonen op het scherm
            data = data_bestand['data']

            # de data volledig aggregeren
            data_geaggregeerd, fouten = aggregeren_volledig(data, definitie_bestand)

        if fouten:
            return render_template("index.html", errormessages=fouten)

        # Zoek omschrijvingen bij de codes zodat we deze in de tabel kunnen tonen
        codelijsten = {}

        for naam, codelijst in definitie_bestand['codelijsten'].items():
            codelijsten[naam] = Codelijst(codelijst['codelijst'])

        lasten = DraaiTabel(
            naam='lasten',
            data=data_geaggregeerd['lasten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['taakveld'],
            kolom_codelijst=codelijsten['categorie_lasten'])

        balans_lasten = DraaiTabel(
            naam='balans_lasten',
            data=data_geaggregeerd['balans_lasten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['categorie_lasten'])

        baten = DraaiTabel(
            naam='baten',
            data=data_geaggregeerd['baten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['taakveld'],
            kolom_codelijst=codelijsten['categorie_baten'])

        balans_baten = DraaiTabel(
            naam='balans_baten',
            data=data_geaggregeerd['balans_baten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['categorie_baten'])

        balans_standen = DraaiTabel(
            naam='balans_standen',
            data=data_geaggregeerd['balans_standen'],
            rij_naam='balanscode',
            kolom_naam='standper',
            rij_codelijst=codelijsten['balanscode'],
            kolom_codelijst=codelijsten['standper'])

        # Voer controles uit
        plausibiliteitscontroles = [PlausibiliteitsControle(controle['omschrijving'],
                                                            controle['definitie'])
                                    for controle in definitie_bestand['controlelijst']['controles']]
        controle_resultaten = [controle.run(data_geaggregeerd) for controle in plausibiliteitscontroles]

        metadata = data_bestand['metadata']
        contact = data_bestand['contact']
        sjabloon_meta = definitie_bestand['metadata']

        # Render sjabloon
        params = {
            'lasten': lasten,
            'balans_lasten': balans_lasten,
            'baten': baten,
            'balans_baten': balans_baten,
            'balans_standen': balans_standen,
            'controle_resultaten': controle_resultaten,
            'bestandsnaam': jsonbestandsnaam,
            'meta': metadata,
            'contact': contact,
            'tabnaam': tabnaam,

            # hebben we onderstaande nog nodig?
            'data': data_bestand,
            'sjabloon': sjabloon_meta,
            'errormessage': "",  # TODO bij foutmeldingen geven we index terug
        }

    return render_template("matrix.html", **params)
