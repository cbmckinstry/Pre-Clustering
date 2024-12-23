from flask import Flask, render_template, request, session
import logging
from flask_session import Session
import traceback
import Calculations  # Import your module

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

            # Validate inputs
            Calculations.validate_inputs(vehlist, pers5, pers6)

            # Generate allocations
            allocations = []
            for priority in range(2):
                for order in [None, "asc", "desc"]:
                    for opt2 in [False, True]:
                        for opt1 in [False, True]:
                            allocations.append(Calculations.allocate_groups(vehlist[:].copy(), pers5, pers6, priority, order, opt2, opt1))

            for order in [None, "asc", "desc"]:
                for opt2 in [False, True]:
                    for opt1 in [False, True]:
                        allocations.append(Calculations.allocate_groups_simultaneous(vehlist[:].copy(), pers5, pers6, order, opt2, opt1))

            # Find the closest allocation
            results = Calculations.closestalg([pers5, pers6], allocations)

            # Ensure results are valid
            if not results or not isinstance(results, list) or len(results) < 2:
                raise ValueError("Invalid results returned from calculations.")

            sorted_allocations, sorted_spaces, sorted_sizes, number = Calculations.sort_closestalg_output(results)

            # Combine the sorted data into tuples of (size, allocation, space) for the template
            combined_sorted_data = []
            for i in range(len(sorted_sizes)):
                combined_sorted_data.append([sorted_sizes[i], sorted_allocations[i], sorted_spaces[i],number[i]])

            session["sorted_allocations"] = combined_sorted_data
            combos=Calculations.combine([sorted_allocations.copy(),sorted_spaces.copy()],results[1].copy())
            splitvers=Calculations.splitting(combos)
            pairs=splitvers[0]
            threes=splitvers[1]

            session["pairs"]=pairs
            session["threes"]=threes
            # Store results in the session

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
                sorted_allocations=None,
                pairs=None,
                threes=None,
                zip=zip,
                enumerate=enumerate

            )

    return render_template(
        "index.html",
        vehlist=",".join(map(str, session.get("vehlist", []))),  # Convert list to comma-separated string
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        results=session.get("results"),
        sorted_allocations=session.get("sorted_allocations"),
        error_message=None,
        pairs=session.get("pairs"),
        threes=session.get("threes"),
        zip=zip,
        enumerate=enumerate

    )

if __name__ == "__main__":
    app.run(debug=True)
