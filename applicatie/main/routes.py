from flask import render_template, request

from applicatie.logic.controles import controle_met_defbestand
from applicatie.logic.draaitabel import DraaiTabel
from applicatie.logic.inlezen import ophalen_en_controleren_databestand, ophalen_bestand_van_web
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

        # Voer controles uit
        plausibiliteitscontroles = [PlausibiliteitsControle(controle['omschrijving'],
                                                            controle['definitie'])
                                    for controle in definitie_bestand['controlelijst']['controles']]
        controle_resultaten = [controle.run(data) for controle in plausibiliteitscontroles]

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
            'data': data_bestand,
            'meta': metadata,
            'sjabloon': sjabloon_meta,
            'errormessage': "",  # TODO bij foutmeldingen geven we index terug
        }

    return render_template("matrix.html", **params)
