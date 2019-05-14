import io
import json

from flask import render_template, request

from applicatie.logic.codelijst import maak_codelijst
from applicatie.logic.controles import controle_met_defbestand
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand, ophalen_bestand_van_web
from applicatie.logic.aggregeren import aggregeren_volledig
from applicatie.logic.plausibiliteitscontrole import PlausibiliteitsControle
from applicatie.main import bp
from config.configurations import IV3_REPO_PATH, IV3_DEF_FILE


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        # TODO Hack Mutatie verwerken (quick and dirty)
        mutatie = dict(request.form)
        data = json.loads(mutatie.pop('data'))
        waarde_naam = mutatie.pop('waarde_naam')
        mutatie['bedrag'] = float(mutatie['bedrag'])
        data['data'][waarde_naam].append(mutatie)
        jsonbestandsnaam = "gemuteerd.json"
        jsonbestand = io.BytesIO(json.dumps(data).encode('utf-8'))
        return matrix(jsonbestand, jsonbestandsnaam)

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
def matrix(jsonbestand, jsonbestandsnaam):
    """ Haal het JSON-bestand op en geef evt. foutmeldingen terug
    Indien geen fouten, laad de pagina met een overzicht van de data.
    """

    print("jsonbestandsnaam = {!r}".format(jsonbestandsnaam))
    print("jsonbestand = {!r}".format(jsonbestand))

    if jsonbestand:
        # json data bestand ophalen en evt. fouten teruggeven

        data_bestand, fouten = ophalen_en_controleren_databestand(jsonbestand)
        # if isinstance(jsonbestand, str):
        # else:
        #     data_bestand = jsonbestand
        #     fouten = []

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
        omschrijvingen = {}

        # TODO Misschien goed idee om een klasse Codelijst te maken
        for naam, codelijst in definitie_bestand['codelijsten'].items():
            omschrijvingen[naam] = maak_codelijst(codelijst['codelijst'])

        # TODO Hier geen dubbele punt erin zetten, ergens anders oplossen
        lasten = DraaiTabel(
            data=data_geaggregeerd['lasten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_omschrijvingen=omschrijvingen['taakveld'],
            kolom_omschrijvingen=omschrijvingen['categorie_lasten'])

        balans_lasten = DraaiTabel(
            data=data_geaggregeerd['balans_lasten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_omschrijvingen=omschrijvingen['balanscode'],
            kolom_omschrijvingen=omschrijvingen['categorie_baten'])

        baten = DraaiTabel(
            data=data_geaggregeerd['baten'],
            rij_naam='taakveld',
            kolom_naam='categorie',
            rij_omschrijvingen=omschrijvingen['taakveld'],
            kolom_omschrijvingen=omschrijvingen['categorie_baten'])

        balans_baten = DraaiTabel(
            data=data_geaggregeerd['balans_baten'],
            rij_naam='balanscode',
            kolom_naam='categorie',
            rij_omschrijvingen=omschrijvingen['balanscode'],
            kolom_omschrijvingen=omschrijvingen['categorie_lasten'])

        balans_standen = DraaiTabel(
            data=data_geaggregeerd['balans_standen'],
            rij_naam='balanscode',
            kolom_naam='standper',
            rij_omschrijvingen=omschrijvingen['balanscode'],
            kolom_omschrijvingen=omschrijvingen['standper'])

        # Voer controles uit
        plausibiliteitscontroles = [PlausibiliteitsControle(controle['omschrijving'],
                                                            controle['definitie'])
                                    for controle in definitie_bestand['controlelijst']['controles']]
        controle_resultaten = [controle.run(data_geaggregeerd) for controle in plausibiliteitscontroles]

        metadata = data_bestand['metadata']
        sjabloon_meta = definitie_bestand['metadata']

        # Render sjabloon
        params = {
            'lasten': lasten,
            'balans_lasten': balans_lasten,
            'baten': baten,
            'balans_baten': balans_baten,
            'balans_standen': balans_standen,
            'controle_resultaten': controle_resultaten,

            # hebben we onderstaande nog nodig?
            'filenaam': jsonbestandsnaam,
            'data': data_bestand,
            'meta': metadata,
            'sjabloon': sjabloon_meta,
            'errormessage': "",  # TODO bij foutmeldingen geven we index terug
        }

    return render_template("matrix.html", **params)
