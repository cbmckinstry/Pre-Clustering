from flask import Flask, request, render_template

import Calculations

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
            results = Calculations.needed(vehlist, pers5, pers6)[0]

            # Generate example configurations
            example_config = Calculations.needed(vehlist, pers5, pers6)[1]

            spaces=Calculations.spaces(example_config,vehlist)
    except Exception as e:
        # Log the error and provide user feedback
        app.logger.error(f"Error processing request: {e}")
        results = [f"Error: {str(e)}"]

    return render_template("index.html", results=results, example_config=example_config, spaces=spaces, vehlist=request.form.get("vehlist", ""), pers5=request.form.get("pers5", ""), pers6=request.form.get("pers6", ""))