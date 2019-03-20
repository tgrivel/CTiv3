from flask import render_template, request
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand
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
    """ Haal het JSON-bestand op en geef evt. foutmeldingen terug
    Indien geen fouten, laad de pagina met een overzicht van de data.
    """

    if jsonbestand:
        # json data bestand ophalen en evt. fouten teruggeven
        databestand, fouten = ophalen_en_controleren_databestand(jsonbestand)
        if fouten:
            return render_template("index.html", errormessages=fouten)

        # json bestand is opgehaald en geen fouten zijn gevonden
        # vervolgens data aggregeren en tonen op het scherm
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

        metadata = databestand['metadata']
        sjabloon_meta = []

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
