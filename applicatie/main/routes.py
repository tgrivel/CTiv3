from flask import render_template, request
from applicatie.logic.inlezen import laad_json_bestand, ophalen_definitiebestand, indikken_data
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
        errormessage = ''
        # definitiebestand = ophalen_definitiebestand(metadata)
        # if isinstance(definitiebestand, str):
        #     errormessage = definitiebestand
        #     return render_template("index.html", errormessage=errormessage)
        # else:
        #     sjabloon_meta = definitiebestand['metadata']

        # compacte_data = indikken_data(complete_upload['waarden'])
        print('stap 1')
        # lasten_header = {'kolkop': maak_lijst_koppen(definitiebestand, "LastenCategorie")}
        # baten_header = {'kolkop': maak_lijst_koppen(definitiebestand, "BatenCategorie")}
        # balans_header = {'kolkop': maak_lijst_koppen(definitiebestand, "BalansDatum")}
        # rekening_rijen = {'rijkop': maak_lijst_koppen(definitiebestand, 'Taakveld')}
        # balans_rijen = {'rijkop': maak_lijst_koppen(definitiebestand, 'Balanscode')}
        print('stap 2')
        # lasten_tabel = maak_tabel(compacte_data, 'Lasten', lasten_header, rekening_rijen)
        # baten_tabel = maak_tabel(compacte_data, 'Baten', baten_header, rekening_rijen)
        # balans_lasten_tabel = maak_tabel(compacte_data, 'balans_lasten', lasten_header, balans_rijen)
        # balans_baten_tabel = maak_tabel(compacte_data, 'balans_baten', baten_header, balans_rijen)
        # balans_standen_tabel = maak_tabel(compacte_data, 'balans_standen', balans_header, balans_rijen)
        # data1 = data # dit is nep-data, niet ingelezen
        print('stap 3')

        lasten = DraaiTabel(
            complete_upload['data']['lasten'],
            aggregeer_kolommen=['taakveld', 'categorie'])
        balans_lasten = DraaiTabel(
            complete_upload['data']['balans_lasten'],
            aggregeer_kolommen=['balanscode', 'categorie'])
        baten = DraaiTabel(
            complete_upload['data']['baten'],
            aggregeer_kolommen=['taakveld', 'categorie'])
        balans_baten = DraaiTabel(
            complete_upload['data']['balans_baten'],
            aggregeer_kolommen=['balanscode', 'categorie'])
        balans_stand = DraaiTabel(
            complete_upload['data']['balans_stand'],
            aggregeer_kolommen=['balanscode', 'standper'])

        tabellen = {
            'lasten': lasten,
            'balans_lasten': balans_lasten,
            'baten': baten,
            'balans_baten': balans_baten,
            'balans_stand': balans_stand,
        }

        # lasten_header = lasten.kolommen

        sjabloon_meta = {
            "Type": 1,
            "Overheidslaag": 1,
            "boekjaar": 1,
        }

        lasten_header = []
        baten_header = []
        balans_header = []
        lasten_tabel = []
        baten_tabel = []
        balans_lasten_tabel = []
        balans_baten_tabel = []
        balans_standen_tabel = []

        params = {
            'lasten': lasten,  # Is alles wat ik nodig heb
            'lasten_header': lasten_header,
            'baten_header': baten_header,
            'balans_header': balans_header,
            'lasten_tabel': lasten_tabel,
            'baten_tabel': baten_tabel,
            'balans_lasten_tabel': balans_lasten_tabel,
            'balans_baten_tabel': balans_baten_tabel,
            'balans_standen_tabel': balans_standen_tabel,
            'data': complete_upload,
            'meta': metadata,
            'sjabloon': sjabloon_meta,
            # 'errormessage': errormessage,
        }

    return render_template("matrix.html", **params)
