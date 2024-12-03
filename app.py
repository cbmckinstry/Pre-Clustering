from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from Calculations import needed, spaces

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"  # Replace with a strong key in production
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    example_configs = None
    remaining_spaces = None
    vehlist = ""
    pers5 = ""
    pers6 = ""
    try:
        if request.method == "POST":
            # Get inputs from the form
            vehlist = request.form["vehlist"]
            pers5 = request.form["pers5"]
            pers6 = request.form["pers6"]

            # Parse inputs
            vehlist = list(map(int, vehlist.split(",")))  # Convert comma-separated input to a list of integers
            pers5 = int(pers5)
            pers6 = int(pers6)

            # Call needed function
            results_data = needed(vehlist, pers5, pers6)
            results = results_data[0]  # [final, other]
            example_configs = results_data[1]  # List of example configurations

            # Calculate remaining spaces for all example configurations
            remaining_spaces = [spaces(config, vehlist) for config in example_configs]

            # Store in session for navigation
            session["example_configs"] = example_configs
            session["current_index"] = 0
            session["remaining_spaces"] = remaining_spaces
    except Exception as e:
        # Log the error and provide user feedback
        app.logger.error(f"Error processing request: {e}")
        results = [f"Error: {str(e)}"]

    return render_template(
        "index.html",
        results=results,
        example_configs=example_configs,
        remaining_spaces=remaining_spaces,
        vehlist=request.form.get("vehlist", ""),
        pers5=request.form.get("pers5", ""),
        pers6=request.form.get("pers6", "")
    )

@app.route("/next")
def next_config():
    if "example_configs" in session:
        session["current_index"] += 1
        if session["current_index"] >= len(session["example_configs"]):
            session["current_index"] = 0  # Loop back to the first configuration
    return redirect(url_for("index"))