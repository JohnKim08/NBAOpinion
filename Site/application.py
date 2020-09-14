from flask import Flask, redirect, url_for, render_template, request, jsonify 

from flask import Markup
import Engine


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    team = request.form.get("team")
    name = request.form.get("name")
    results = Engine.get_results(name,team)
    #Probably need to add seasons and their dates
    return render_template("result.html", name=name, team=team, results=results)



if __name__  == "__main__":
    app.run()


    