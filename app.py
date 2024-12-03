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
        session["pers5"] = ""
        session["pers6"] = ""
        session["results"] = None

    example_configs = session.get("example_configs", [])
    remaining_spaces = session.get("remaining_space", [])
    results = session.get("results", None)
    vehlist = session.get("vehlist", [])
    pers5 = session.get("pers5", "")
    pers6 = session.get("pers6", "")
    error_message = None

    # Convert vehlist to a string for display in the form
    vehlist_display = ",".join(map(str, vehlist)) if vehlist else ""

    try:
        if request.method == "POST":
            # Get inputs from the form
            vehlist = request.form.get("vehlist", "").strip()
            pers5 = request.form.get("pers5", "").strip()
            pers6 = request.form.get("pers6", "").strip()

            # Validate vehlist
            try:
                vehlist_list = [
                    int(value.strip()) for value in vehlist.split(",") if value.strip() != ""
                ]
                if any(v < 0 for v in vehlist_list):
                    raise ValueError("All vehicle capacities must be nonnegative integers.")
            except ValueError as ve:
                error_message = (
                    "Please enter a properly formatted comma-separated list of nonnegative integers for vehicle capacities."
                )
                app.logger.error(f"Validation error for vehlist: {ve}")
                raise Exception(error_message)

            # Validate pers5
            try:
                pers5 = int(pers5) if pers5 else 0
                if pers5 < 0:
                    raise ValueError("The number of 5-person crews must be a nonnegative integer.")
            except ValueError as ve:
                error_message = "Please enter a nonnegative integer for the number of 5-person crews."
                app.logger.error(f"Validation error for pers5: {ve}")
                raise Exception(error_message)

            # Validate pers6
            try:
                pers6 = int(pers6) if pers6 else 0
                if pers6 < 0:
                    raise ValueError("The number of 6-person crews must be a nonnegative integer.")
            except ValueError as ve:
                error_message = "Please enter a nonnegative integer for the number of 6-person crews."
                app.logger.error(f"Validation error for pers6: {ve}")
                raise Exception(error_message)

            # Calculate configurations
            results_data = needed(vehlist_list, pers5, pers6)
            results = results_data[0]
            example_configs = results_data[1]

            # Calculate remaining space for each configuration
            remaining_spaces = [spaces(config, vehlist_list) for config in example_configs]

            # Store data in session
            session["vehlist"] = vehlist_list
            session["pers5"] = pers5
            session["pers6"] = pers6
            session["example_configs"] = example_configs
            session["current_index"] = 0
            session["remaining_space"] = remaining_spaces[0] if remaining_spaces else []
            session["results"] = results

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        if not error_message:
            error_message = "An unexpected error occurred. Please check your input."

    return render_template(
        "index.html",
        results=results,
        example_configs=example_configs,
        remaining_spaces=remaining_spaces,
        vehlist=vehlist_display,
        pers5=pers5,
        pers6=pers6,
        error_message=error_message
    )


@app.route("/next", methods=["GET"])
def next_config():
    try:
        # Check if necessary session data exists
        if "example_configs" not in session or not session["example_configs"]:
            raise Exception("No configurations available. Please submit the form first.")

        if "vehlist" not in session or not session["vehlist"]:
            raise Exception("Vehicle capacities are missing. Please submit the form first.")

        # Retrieve and validate session data
        example_configs = session["example_configs"]
        vehlist = session["vehlist"]
        current_index = session.get("current_index", 0)

        # Increment current index
        current_index += 1
        if current_index >= len(example_configs):
            current_index = 0  # Loop back to the first configuration

        # Update remaining spaces for the current configuration
        session["current_index"] = current_index
        current_config = example_configs[current_index]
        session["remaining_space"] = spaces(current_config, vehlist)

    except Exception as e:
        app.logger.error(f"An error occurred in next_config: {e}")
        return redirect(url_for("index"))  # Redirect back to the main page with the form

    return redirect(url_for("index"))