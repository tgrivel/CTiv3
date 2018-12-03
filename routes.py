from flask import Flask, render_template, request

from Verwerking.inlezen import ophalen_file, ophalen_sjabloon
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
    if bestandsnaam:
        meta = ophalen_file(bestandsnaam)
        sjabloon = ophalen_sjabloon(meta)
        print ('sjabloon', sjabloon)
    return render_template("matrix.html", x = data, h = header, meta = meta, sjabloon = sjabloon)

if __name__ == "__main__":
    app.run(debug = True)