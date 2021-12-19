from flask import Flask,render_template, url_for,request,redirect
import sys
import pickle
import numpy as np
import nlp

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("init.html")

@app.route("/show")
def show():
    bar = nlp.visual()
    return render_template("show.html",plot = bar)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
