from flask import Flask, render_template, request

from Verwerking.inlezen import laad_json_bestand, ophalen_sjabloon
from Verwerking.maak_matrix import data, header

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        return matrix(bestandsnaam=request.files['file'])
    elif request.method == 'GET':
        return render_template("index.html")

@app.route("/matrix", methods = ['GET','POST'])
def matrix(bestandsnaam):
    """Laad de pagina met een overzicht."""
    if bestandsnaam:
        data2 = laad_json_bestand(bestandsnaam)
        metadata = data2['metadata']
        sjabloon = ophalen_sjabloon(metadata)
        data1 = data # dit is nep-data, niet ingelezen

        # TODO Dit moet nog wat mooier
        params = {
            'data': data2,
            'x': data1,
            'h': header,
            'meta': metadata,
            'sjabloon': sjabloon,
            # 'taakvelden': hoofdtaakvelden
        }

    return render_template("matrix.html", **params)

if __name__ == "__main__":
    app.run(debug=True)