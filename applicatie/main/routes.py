from flask import render_template, request

from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_definitiebestand, ophalen_databestand
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
        databestand, foutmeldingen_databestand = ophalen_databestand(jsonbestand)

        if foutmeldingen_databestand:
            return render_template("index.html", errormessages=foutmeldingen_databestand)

        # definitiebestand ophalen
        metadata = databestand['metadata']
        definitiebestand, foutmeldingen_definitiebestand = ophalen_definitiebestand(metadata)

        if foutmeldingen_definitiebestand:
            return render_template("index.html", errormessages=foutmeldingen_definitiebestand)

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
