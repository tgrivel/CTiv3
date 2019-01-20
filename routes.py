from flask import Flask, render_template, request

from Verwerking.inlezen import laad_json_bestand, ophalen_sjabloon, indikken_data
from Verwerking.maak_matrix import maak_tabel, maak_lijst_koppen

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            print("proberen naar matrix te gaan")
            return matrix(bestandsnaam=request.files['file'])
        except:
            return render_template("index.html")
    elif request.method == 'GET':
        return render_template("index.html")

@app.route("/matrix", methods = ['GET','POST'])
def matrix(bestandsnaam):
    """Laad de pagina met een overzicht."""
    if bestandsnaam:
        complete_upload = laad_json_bestand(bestandsnaam)
        metadata = complete_upload['metadata']
        sjabloon = ophalen_sjabloon(metadata)
        sjabloon_meta = sjabloon['metadata']
        compacte_data = indikken_data(complete_upload['waarden'])
        print('stap 1')
        lasten_header = {'kolkop': maak_lijst_koppen(sjabloon,"LastenCategorien")}
        baten_header = {'kolkop': maak_lijst_koppen(sjabloon,"BatenCategorien")}
        balans_header = {'kolkop': maak_lijst_koppen(sjabloon,"BalansDatums")}
        rekening_rijen = {'rijkop': maak_lijst_koppen(sjabloon,'Taakvelden')}
        balans_rijen = {'rijkop': maak_lijst_koppen(sjabloon,'Balanscodes')}
        print('stap 2')
        lasten_tabel = maak_tabel(compacte_data, 'lasten',lasten_header, rekening_rijen)
        baten_tabel = maak_tabel(compacte_data, 'baten', baten_header, rekening_rijen)
        balans_lasten_tabel = maak_tabel(compacte_data, 'balans_lasten', lasten_header, balans_rijen)
        balans_baten_tabel = maak_tabel(compacte_data, 'balans_baten', baten_header, balans_rijen)
        balans_standen_tabel = maak_tabel(compacte_data, 'balans_standen', balans_header, balans_rijen)
        # data1 = data # dit is nep-data, niet ingelezen
        print('stap 3')

        params = {
            'lasten_header': lasten_header,
            'baten_header': baten_header,
            'balans_header': balans_header,
            'lasten_tabel':lasten_tabel,
            'baten_tabel': baten_tabel,
            'balans_lasten_tabel': balans_lasten_tabel,
            'balans_baten_tabel': balans_baten_tabel,
            'balans_standen_tabel': balans_standen_tabel,
            'data': complete_upload,
            'meta': metadata,
            'sjabloon': sjabloon_meta,

        }

    return render_template("matrix.html", **params)

if __name__ == "__main__":
    app.run(debug=True)