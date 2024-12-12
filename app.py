from flask import Flask, render_template, request, session
import logging
from flask_session import Session
import traceback
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
            # Input parsing and validation
            vehlist_input = request.form.get("vehlist", "").strip()
            pers5_input = request.form.get("pers5", "").strip()
            pers6_input = request.form.get("pers6", "").strip()

            vehlist = [int(x.strip()) for x in vehlist_input.split(",") if x.strip()]
            pers5 = int(pers5_input) if pers5_input else 0
            pers6 = int(pers6_input) if pers6_input else 0

            Calculations.validate_inputs(vehlist, pers5, pers6)

            # Perform calculations
            allocation1 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0)
            allocation7 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0,"none",True)
            allocation3 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0,"asc")
            allocation8 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0,"asc",True)
            allocation4 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0,"desc")
            allocation9 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 0,"desc",True)
            allocation2 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1)
            allocation10 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1,"none",True)
            allocation5 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1,"asc")
            allocation11 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1,"asc",True)
            allocation6 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1,"desc")
            allocation12 = Calculations.allocate_groups(vehlist[:], pers5, pers6, 1,"desc",True)
            simultaneous_allocation = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6
            )
            simultaneous_allocation3 = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6,"none",True
            )
            simultaneous_allocation1 = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6, "asc"
            )
            simultaneous_allocation4 = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6, "asc",True
            )
            simultaneous_allocation2 = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6, "desc"
            )
            simultaneous_allocation5 = Calculations.allocate_groups_simultaneous(
                vehlist[:], pers5, pers6, "desc",True
            )

            results = Calculations.closestalg(
                [pers5, pers6], [allocation1, allocation2, simultaneous_allocation, simultaneous_allocation1, allocation3, allocation5, allocation4, allocation6, simultaneous_allocation2,allocation7,allocation8,allocation9,allocation10,allocation11,allocation12,simultaneous_allocation3,simultaneous_allocation4,simultaneous_allocation5]
            )

            # Ensure results are valid
            if not results or not isinstance(results, list) or len(results) < 2:
                raise ValueError("Invalid results returned from calculations.")

            session["vehlist"] = vehlist
            session["pers5"] = pers5
            session["pers6"] = pers6
            session["results"] = results

        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            logging.error(traceback.format_exc())
            return render_template(
                "index.html",
                error_message=f"An error occurred: {e}",
                vehlist=vehlist_input,
                pers5=pers5_input,
                pers6=pers6_input,
                results=None,
            )

    return render_template(
        "index.html",
        vehlist=",".join(map(str, session.get("vehlist", []))),  # Convert list to comma-separated string
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        results=session.get("results"),
        error_message=None,
    )