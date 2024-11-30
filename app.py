from flask import Flask, request, render_template

from Calculations import needed
from Calculations import closest

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    example_config = None
    vehlist = ""
    pers5 = ""
    pers6 = ""
    try:
        if request.method == "POST":
            # Get inputs from the form
            vehlist = request.form["vehlist"]
            pers5 = request.form["pers5"]
            pers6 = request.form["pers6"]

            # Parse inputs for the needed function
            vehlist = list(map(int, vehlist.split(",")))  # Convert comma-separated input to a list of integers
            pers5 = int(pers5)
            pers6 = int(pers6)

            # Call the needed function
            results = needed(vehlist, pers5, pers6)

            # Generate example configurations
            example_config = closest(vehlist,[pers5,pers6])  # Replace with actual logic for example configurations
    except Exception as e:
        # Log the error and provide user feedback
        app.logger.error(f"Error processing request: {e}")
        results = [f"Error: {str(e)}"]

    return render_template("index.html", results=results, example_config=example_config, vehlist=request.form.get("vehlist", ""), pers5=request.form.get("pers5", ""), pers6=request.form.get("pers6", ""))