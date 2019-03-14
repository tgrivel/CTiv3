from flask import render_template, request

from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_databestand, ophalen_bestand_van_repo
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
    """Laad de pagina met een overzicht."""
    if jsonbestand:
        # json bestand inlezen
        databestand, fouten_databestand = ophalen_databestand(jsonbestand)

        if fouten_databestand:
            return render_template("index.html", errormessages=fouten_databestand)

        #schemabestand, foutmeldingen_schemabestand = ophalen_schemabestand()

        #foutmeldingen_schemacontrole = controle_met_schema(databestand)

        # definitiebestand ophalen
        metadata = databestand['metadata']
        ovlaag = metadata['overheidslaag']
        boekjaar = metadata['boekjaar']
        bestandsnaam = 'iv3_definities_' + ovlaag + '_' + boekjaar + '.json'
        url = "https://raw.github.com/tgrivel/iv3_modellen/master/"
        definitiebestand, fouten_definitiebestand = ophalen_bestand_van_repo(url, bestandsnaam, 'definitiebetand')

        if fouten_definitiebestand:
            return render_template("index.html", errormessages=fouten_definitiebestand)

        sjabloon_meta = definitiebestand['metadata']

        lasten = DraaiTabel(
            data=databestand['data']['lasten'],
            rij_naam='taakveld', kolom_naam='categorie')
        balans_lasten = DraaiTabel(
            data=databestand['data']['balans_lasten'],
            rij_naam='balanscode', kolom_naam='categorie')
        baten = DraaiTabel(
            data=databestand['data']['baten'],
            rij_naam='taakveld', kolom_naam='categorie')
        balans_baten = DraaiTabel(
            data=databestand['data']['balans_baten'],
            rij_naam='balanscode', kolom_naam='categorie')
        balans_standen = DraaiTabel(
            data=databestand['data']['balans_standen'],
            rij_naam='balanscode', kolom_naam='standper')

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
