from flask import Flask, redirect, url_for, render_template, request, jsonify 

from flask import Markup



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    team = request.form.get("team")
    name = request.form.get("name")
    return render_template("result.html", name=name, team=team )

if __name__  == "__main__":
    app.run()


    