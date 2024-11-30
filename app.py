from flask import Flask, request, render_template

from Calculations import needed

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        try:
            vehlist = list(map(int, request.form["vehlist"].split(",")))
            pers5 = int(request.form["pers5"])
            pers6 = int(request.form["pers6"])
            results = needed(vehlist, pers5, pers6)
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template("index.html", results=results)