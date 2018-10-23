from flask import Flask, render_template, request
from Verwerking.maak_matrix import data
from Verwerking.inlezen import ophalen_file

import os

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            ophalen_file(file)
        return render_template("matrix.html", x = data)
    elif request.method == 'GET':
        return render_template("index.html")

@app.route("/matrix", methods = ['GET','POST'])
def matrix():

    return render_template("matrix.html")




if __name__ == "__main__":
    app.run(debug = True)