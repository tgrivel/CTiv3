from flask import render_template, request
from applicatie.logic.inlezen import laad_json_bestand, ophalen_definitiebestand
from applicatie.logic.maak_matrix import maak_tabel, maak_lijst_koppen, pivot_table
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.main import bp


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.files.get('file', None):
            return render_template("index.html", errormessage='Geen json bestand geselecteerd')
        else:
            jsonfile = request.files['file']
            return matrix(jsonbestand=jsonfile)
    elif request.method == 'GET':
        return render_template("index.html", errormessage='')


@bp.route("/matrix", methods=['GET', 'POST'])
def matrix(jsonbestand):
    """Laad de pagina met een overzicht."""
    if jsonbestand:
        # json bestand inlezen
        complete_upload = laad_json_bestand(jsonbestand)
        metadata = complete_upload['metadata']

        # definitiebestand ophalen
        resultaat = ophalen_definitiebestand(metadata)
        definitiebestand = resultaat[0]
        errormessage = resultaat[1]

        if errormessage != '':
            # we hebben een foutmelding teruggekregen
            return render_template("index.html", errormessage=errormessage)

        sjabloon_meta = definitiebestand['metadata']

        lasten = DraaiTabel(
            data=complete_upload['data']['lasten'],
            rij_naam='taakveld', kolom_naam='categorie')
        balans_lasten = DraaiTabel(
            data=complete_upload['data']['balans_lasten'],
            rij_naam='balanscode', kolom_naam='categorie')
        baten = DraaiTabel(
            data=complete_upload['data']['baten'],
            rij_naam='taakveld', kolom_naam='categorie')
        balans_baten = DraaiTabel(
            data=complete_upload['data']['balans_baten'],
            rij_naam='balanscode', kolom_naam='categorie')
        balans_standen = DraaiTabel(
            data=complete_upload['data']['balans_standen'],
            rij_naam='balanscode', kolom_naam='standper')

        params = {
            'lasten': lasten,  # Is alles wat ik nodig heb
            'balans_lasten': balans_lasten,
            'baten': baten,
            'balans_baten': balans_baten,
            'balans_standen': balans_standen,

            # hebben we onderstaande nog nodig?
            'data': complete_upload,
            'meta': metadata,
            'sjabloon': sjabloon_meta,
            'errormessage': errormessage,
        }

    return render_template("matrix.html", **params)
