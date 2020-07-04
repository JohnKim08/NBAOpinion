from flask import Flask, redirect, url_for
app = Flask(__name__)
@app.route("/")
def home():
    return "Hello World <h1>HELLO<h1>"
@app.route("/<name>")
#Passes it into the webpage
def user(name):
    return f"Hello {name}"
@app.route("/admin")
def admin():
    return redirect(url_for("home"))
if __name__  == "__main__":
    app.run()
    