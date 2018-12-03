from flask import Flask, render_template, request
from Verwerking.maak_matrix import data, header
from Verwerking.inlezen import ophalen_file, ophalen_sjabloon


import os

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            meta = ophalen_file(file)
            sjabloon = ophalen_sjabloon(meta)
            print (sjabloon)
        return render_template("matrix.html", x = data, h = header, meta = meta, sjabloon = sjabloon)
    elif request.method == 'GET':
        return render_template("index.html")

@app.route("/matrix", methods = ['GET','POST'])
def matrix():

    return render_template("matrix.html")

if __name__ == "__main__":
    app.run(debug = True)