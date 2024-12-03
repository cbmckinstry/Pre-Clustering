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
    results = None
    example_configs = None
    remaining_spaces = None
    vehlist = session.get("vehlist", "")
    pers5 = session.get("pers5", "")
    pers6 = session.get("pers6", "")
    try:
        if request.method == "POST":
            # Get inputs from the form
            vehlist = request.form["vehlist"]
            pers5 = request.form["pers5"]
            pers6 = request.form["pers6"]

            # Parse inputs
            vehlist_list = list(map(int, vehlist.split(",")))  # Convert to a list of integers
            pers5 = int(pers5)
            pers6 = int(pers6)

            # Store inputs in session
            session["vehlist"] = vehlist_list
            session["pers5"] = pers5
            session["pers6"] = pers6

            # Call needed function
            results_data = needed(vehlist_list, pers5, pers6)
            results = results_data[0]  # [final, other]
            example_configs = results_data[1]  # List of example configurations

            # Calculate remaining spaces
            remaining_spaces = [spaces(config, vehlist_list) for config in example_configs]

            # Store in session for navigation
            session["example_configs"] = example_configs
            session["current_index"] = 0
            session["remaining_space"] = remaining_spaces[0] if remaining_spaces else []
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        results = [f"Error: {str(e)}"]

    return render_template(
        "index.html",
        results=results,
        example_configs=session.get("example_configs"),
        remaining_spaces=session.get("remaining_space"),
        vehlist=session.get("vehlist", ""),
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", "")
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
    else:
        app.logger.warning("Attempted to access /next without valid session data.")
        return redirect(url_for("index"))
    return redirect(url_for("index"))