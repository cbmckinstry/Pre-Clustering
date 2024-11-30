from flask import Flask, request, render_template

from Calculations import needed

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    vehlist = ""
    pers5 = ""
    pers6 = ""
    if request.method == "POST":
        try:
            vehlist = request.form["vehlist"]
            pers5 = request.form["pers5"]
            pers6 = request.form["pers6"]

            # Parse inputs for the needed function
            vehlist = list(map(int, vehlist.split(",")))
            pers5 = int(pers5)
            pers6 = int(pers6)

            # Call the needed function
            results = needed(vehlist, pers5, pers6)
        except Exception as e:
            results = [f"Error: {str(e)}"]

    return render_template("index.html", results=results, vehlist=request.form.get("vehlist", ""), pers5=request.form.get("pers5", ""), pers6=request.form.get("pers6", ""))