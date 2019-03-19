from flask import render_template, request
from config.configurations import REPO_PATH
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_databestand, ophalen_bestand_van_repo
from applicatie.logic.controles import controle_met_schema
from applicatie.main import bp


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.files.get('file', None):
            return render_template("index.html", errormessages=['Geen json bestand geselecteerd'])
        else:
            jsonfile = request.files['file']
            return matrix(jsonbestand=jsonfile)
    elif request.method == 'GET':
        return render_template("index.html", errormessages=[])


@bp.route("/matrix", methods=['GET', 'POST'])
def matrix(jsonbestand):
    """Laad de pagina met een overzicht van de data.
    Voer eerst diverse controles uit
    en geef evt. foutmeldingen terug:
        - json data bestand inlezen
        - json schema ophalen van repo
        - json data controleren aan json schema
        - json definitie bestand ophalen van repo
        - TODO: json data controleren aan het definitiebestand
    """
    if jsonbestand:
        # json data bestand inlezen
        databestand, fouten_databestand = ophalen_databestand(jsonbestand)
        if fouten_databestand:
            return render_template("index.html", errormessages=fouten_databestand)

        # json schema ophalen van repo
        bestandsnaam = 'iv3_data_schema_v1_0.json'
        schemabestand, fouten_schemabestand = ophalen_bestand_van_repo(REPO_PATH, bestandsnaam, 'schemabestand')
        if fouten_schemabestand:
            return render_template("index.html", errormessages=fouten_schemabestand)

        # json data controleren aan json schema
        fouten_schemacontrole = controle_met_schema(databestand, schemabestand)
        if fouten_schemacontrole:
            return render_template("index.html", errormessages=fouten_schemacontrole)

        # json definitie bestand ophalen van repo
        metadata = databestand['metadata']
        overheidslaag = metadata['overheidslaag']
        boekjaar = metadata['boekjaar']
        bestandsnaam = 'iv3_definities_' + overheidslaag + '_' + boekjaar + '.json'
        definitiebestand, fouten_definitiebestand = ophalen_bestand_van_repo(REPO_PATH, bestandsnaam, 'definitiebetand')
        if fouten_definitiebestand:
            return render_template("index.html", errormessages=fouten_definitiebestand)

        # json data controleren aan het definitiebestand
        sjabloon_meta = definitiebestand['metadata']
        # TODO: nog niet klaar

        # alle controles zijn uitgevoerd.
        # nu data aggregeren en tonen op het scherm
        data = databestand['data']
        lasten = DraaiTabel(
            data=data['lasten'], rij_naam='taakveld', kolom_naam='categorie')
        balans_lasten = DraaiTabel(
            data=data['balans_lasten'], rij_naam='balanscode', kolom_naam='categorie')
        baten = DraaiTabel(
            data=data['baten'], rij_naam='taakveld', kolom_naam='categorie')
        balans_baten = DraaiTabel(
            data=data['balans_baten'], rij_naam='balanscode', kolom_naam='categorie')
        balans_standen = DraaiTabel(
            data=data['balans_standen'], rij_naam='balanscode', kolom_naam='standper')

        params = {
            'lasten': lasten,
            'balans_lasten': balans_lasten,
            'baten': baten,
            'balans_baten': balans_baten,
            'balans_standen': balans_standen,

            # hebben we onderstaande nog nodig?
            'data': databestand,
            'meta': metadata,
            'sjabloon': sjabloon_meta,
            'errormessage': "",  # TODO bij foutmeldingen geven we index terug
        }

    return render_template("matrix.html", **params)
