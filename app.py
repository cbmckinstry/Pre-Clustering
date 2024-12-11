from flask import Flask, render_template, request, session
import logging
from flask_session import Session
import Calculations

# Configure Flask and Logging
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"
Session(app)

logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get user inputs from the form
            vehlist_input = request.form.get("vehlist", "").strip()
            pers5_input = request.form.get("pers5", "").strip()
            pers6_input = request.form.get("pers6", "").strip()

            # Parse inputs
            vehlist = [int(x.strip()) for x in vehlist_input.split(",") if x.strip()]
            pers5 = int(pers5_input) if pers5_input else 0
            pers6 = int(pers6_input) if pers6_input else 0

            # Validate inputs
            Calculations.validate_inputs(vehlist, pers5, pers6)

            # Perform calculations using updated functions
            allocation1 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0)
            allocation2 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1)
            simultaneous_allocation = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6
            )

            # Use closestalg to find the best allocation
            allocations = [allocation1, allocation2, simultaneous_allocation]
            results = Calculations.closestalg([pers5, pers6], allocations)

            # Update session for display
            session["vehlist"] = vehlist
            session["pers5"] = pers5
            session["pers6"] = pers6
            session["results"] = results

        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return render_template(
                "index.html",
                error_message=f"An error occurred: {e}",
                vehlist=vehlist_input,
                pers5=pers5_input,
                pers6=pers6_input,
                results=None,
            )

    # Retrieve session data for rendering
    return render_template(
        "index.html",
        vehlist=session.get("vehlist", ""),
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        results=session.get("results", None),
        error_message=None,
    )


if __name__ == "__main__":
    app.run(debug=True)