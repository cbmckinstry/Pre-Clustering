import logging
from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from Calculations import needed, spaces

# Configure Flask and logging
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"  # Replace with a strong key in production
Session(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return "An internal error occurred. Please check the logs for details.", 500

# Configure session to use filesystem
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"  # Replace with a strong key in production
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if "example_configs" not in session:
        # Initialize session keys to prevent KeyError
        session["example_configs"] = []
        session["remaining_space"] = []
        session["current_index"] = 0
        session["vehlist"] = []
        session["pers5"] = 0
        session["pers6"] = 0
        session["results"] = None

    example_configs = session.get("example_configs", [])
    remaining_spaces = session.get("remaining_space", [])
    results = session.get("results", None)
    vehlist = session.get("vehlist", "")
    pers5 = session.get("pers5", 0)
    pers6 = session.get("pers6", 0)

    try:
        if request.method == "POST":
            # Get inputs from the form
            vehlist = request.form.get("vehlist", "").split(",")
            pers5 = request.form.get("pers5", 0)
            pers6 = request.form.get("pers6", 0)

            # Parse inputs
            vehlist = list(map(int, vehlist))
            pers5 = int(pers5)
            pers6 = int(pers6)

            # Calculate configurations
            results_data = needed(vehlist, pers5, pers6)
            results = results_data[0]
            example_configs = results_data[1]

            # Calculate remaining space for each configuration
            remaining_spaces = [spaces(config, vehlist) for config in example_configs]

            # Store data in session
            session["vehlist"] = vehlist
            session["pers5"] = pers5
            session["pers6"] = pers6
            session["example_configs"] = example_configs
            session["current_index"] = 0
            session["remaining_space"] = remaining_spaces[0] if remaining_spaces else []
            session["results"] = results
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")

    # Convert vehlist back to a comma-separated string for the template
    vehlist_str = ",".join(map(str, session.get("vehlist", [])))

    return render_template(
        "index.html",
        results=results,
        example_configs=example_configs,
        remaining_spaces=remaining_spaces,
        vehlist=vehlist_str,
        pers5=pers5,
        pers6=pers6
    )

@app.route("/next", methods=["GET"])
def next_config():
    if "example_configs" in session:
        session["current_index"] += 1
        if session["current_index"] >= len(session["example_configs"]):
            session["current_index"] = 0  # Loop back to the first configuration

        # Update remaining space for the current configuration
        current_index = session["current_index"]
        vehlist = session.get("vehlist", [])
        example_config = session["example_configs"][current_index]
        session["remaining_space"] = spaces(example_config, vehlist)
    return redirect(url_for("index"))