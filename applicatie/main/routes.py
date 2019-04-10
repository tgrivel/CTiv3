from flask import render_template, request

from applicatie.logic.controles import controle_met_defbestand
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand, ophalen_bestand_van_web
from applicatie.logic.aggregeren import aggregeren_volledig
from applicatie.logic.plausibiliteitscontrole import PlausibiliteitsControle
from applicatie.main import bp
from config.configurations import IV3_REPO_PATH, IV3_DEF_FILE


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.files.get('file', None):
            return render_template("index.html", errormessages=['Geen json bestand geselecteerd'])
        else:
            jsonfile = request.files['file']
            jsonfilename = jsonfile.filename
            return matrix(jsonbestand=jsonfile, jsonbestandsnaam=jsonfilename)
    elif request.method == 'GET':
        return render_template("index.html", errormessages=[])


@bp.route("/matrix", methods=['GET', 'POST'])
def matrix(jsonbestand, jsonbestandsnaam):
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
            definitie_bestand, fouten = ophalen_bestand_van_web(IV3_REPO_PATH, bestandsnaam, 'definitiebetand')

        if not fouten:
            # Controle databestand met definitiebestand
            fouten = controle_met_defbestand(data_bestand, definitie_bestand)

        if fouten:
            return render_template("index.html", errormessages=fouten)

        # json bestand is opgehaald en geen fouten zijn gevonden
        # vervolgens data aggregeren en tonen op het scherm
        data = data_bestand['data']

        # de data volledig aggregeren
        data_geaggregeerd, fouten = aggregeren_volledig(data, definitie_bestand)
        if fouten:
            return render_template("index.html", errormessages=fouten)

        # per rekening de data aggregeren over de opgegeven dimensies
        # N.B. de dimensies eindigend op ':' bevatten de code + de omschrijving van de code
        # in de rijen van de matrix willen we namelijk ook de omschrijving tonen

        lasten = DraaiTabel(
            data=data_geaggregeerd['lasten'],
            rij_naam='taakveld' + ':',              # taakveld inclusief omschrijving
            kolom_naam='categorie')

        balans_lasten = DraaiTabel(
            data=data_geaggregeerd['balans_lasten'],
            rij_naam='balanscode' + ':',            # balanscode inclusief omschrijving
            kolom_naam='categorie')

        baten = DraaiTabel(
            data=data_geaggregeerd['baten'],
            rij_naam='taakveld' + ':',              # taakveld inclusief omschrijving
            kolom_naam='categorie')

        balans_baten = DraaiTabel(
            data=data_geaggregeerd['balans_baten'],
            rij_naam='balanscode' + ':',            # balanscode inclusief omschrijving
            kolom_naam='categorie')

        balans_standen = DraaiTabel(
            data=data_geaggregeerd['balans_standen'],
            rij_naam='balanscode' + ':',            # balanscode inclusief omschrijving
            kolom_naam='standper')

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
