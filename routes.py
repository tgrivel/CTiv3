from flask import Flask, render_template, request
from collections import OrderedDict
import json

import os


app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print(file.filename)
            newfiel = file.read()
            #data = json.loads(newfiel.decode('utf-8'))
            data = json.loads(newfiel.decode('cp1251'))
            verwerken(data)
            # newfiel = file.read()
            # data = json.load(newfiel, object_pairs_hook=OrderedDict)
            # verwerken(data)
            #
            # with open(newfiel) as bron:
            #     data = json.load(bron, object_pairs_hook=OrderedDict)
            #     verwerken(data)
    return render_template("index.html")

@app.route("/matrix")
def matrix():
    return render_template("matrix.html")


def verwerken(data):
    aantal = 0
    for row in data:
        aantal += 1
    print('totaal ' + str(aantal) + ' ingelezen')

if __name__ == "__main__":
    app.run(debug = True)