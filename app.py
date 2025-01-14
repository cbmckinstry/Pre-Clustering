from flask import Flask, render_template, request, session
import logging
from flask_session import Session
import traceback
from Master import *
from Allocations import *

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
            pers7_input = request.form.get("pers7", "").strip()

            vehlist = [int(x.strip()) for x in vehlist_input.split(",") if x.strip()]
            pers5 = int(pers5_input) if pers5_input else 0
            pers6 = int(pers6_input) if pers6_input else 0
            pers7 = int(pers7_input) if pers7_input else 0

            # Validate inputs
            validate_inputs(vehlist, pers5, pers6, pers7)

            # Determine backup group and primary group
            backup_group = pers7 if pers7 != 0 else pers5
            primary_group = pers6
            use_backup = pers7 != 0

            # Generate allocations
            allocations = []
            for priority in range(2):
                for order in [None, "asc", "desc"]:
                    for opt2 in [False, True]:
                        for opt1 in [False, True]:
                            allocations.append(allocate_groups(
                                vehlist[:].copy(), backup_group, primary_group, priority, order, opt2, opt1, use_backup
                            ))

            for order in [None, "asc", "desc"]:
                for opt2 in [False, True]:
                    for opt1 in [False, True]:
                        allocations.append(allocate_groups_simultaneous(
                            vehlist[:].copy(), backup_group, primary_group, order, opt2, opt1, use_backup
                        ))

            # Closest allocation logic
            backupsize = 5 if pers7 == 0 else 7
            results = closestalg([backup_group, pers6], allocations,backupsize)
            if not results or not isinstance(results, list) or len(results) < 2:
                raise ValueError("Invalid results returned from calculations.")

            sorted_allocations, sorted_spaces, sorted_sizes, number = sort_closestalg_output(results, backupsize)

            # Combine the sorted data for the template
            combined_sorted_data = [
                [sorted_sizes[i], sorted_allocations[i], sorted_spaces[i], number[i]]
                for i in range(len(sorted_sizes))
            ]

            # Store sorted allocations and results in session
            session["sorted_allocations"] = combined_sorted_data
            pairs,threes=allalgs(sorted_allocations.copy(),sorted_spaces,results[1].copy(),backupsize)
            session["pairs"] = pairs
            session["threes"]=threes
            session["vehlist"] = vehlist
            session["pers5"] = pers5
            session["pers6"] = pers6
            session["pers7"] = pers7
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
                pers7=pers7_input,
                results=None,
                sorted_allocations=None,
                pairs=None,
                threes=None,
                matrices_result=session.get("matrices_result"),
                ranges_result=session.get("ranges_result"),
                total_people=session.get("total_people", ""),
                people=session.get("people", ""),
                crews=session.get("crews", ""),
                zip=zip,
                enumerate=enumerate
            )

    return render_template(
        "index.html",
        vehlist=",".join(map(str, session.get("vehlist", []))),
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        pers7=session.get("pers7", ""),
        results=session.get("results"),
        sorted_allocations=session.get("sorted_allocations"),
        error_message=None,
        pairs=session.get("pairs"),
        threes=session.get("threes"),
        matrices_result=session.get("matrices_result"),
        ranges_result=session.get("ranges_result"),
        total_people=session.get("total_people", ""),
        people=session.get("people", ""),
        crews=session.get("crews", ""),
        zip=zip,
        enumerate=enumerate
    )
@app.route("/matrices", methods=["POST"])
def matrices():
    try:
        # Input parsing
        people_input = request.form.get("people", "").strip()
        crews_input = request.form.get("crews", "").strip()

        people = int(people_input) if people_input else 0
        crews = int(crews_input) if crews_input else 0

        # Run matrices algorithm
        matrices_result = matrices(people, crews)

        # Store the result in session
        session["matrices_result"] = matrices_result
        session["people"] = people
        session["crews"] = crews

    except Exception as e:
        logging.error(f"Exception occurred while running matrices: {e}")
        logging.error(traceback.format_exc())
        return render_template(
            "index.html",
            error_message=f"An error occurred while running matrices: {e}",
            vehlist=",".join(map(str, session.get("vehlist", []))),
            pers5=session.get("pers5", ""),
            pers6=session.get("pers6", ""),
            pers7=session.get("pers7", ""),
            results=session.get("results"),
            sorted_allocations=session.get("sorted_allocations"),
            pairs=session.get("pairs"),
            threes=session.get("threes"),
            matrices_result=None,
            ranges_result=session.get("ranges_result"),
            total_people=session.get("total_people", ""),
            people=people_input,
            crews=crews_input,
            zip=zip,
            enumerate=enumerate
        )

    return render_template(
        "index.html",
        vehlist=",".join(map(str, session.get("vehlist", []))),
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        pers7=session.get("pers7", ""),
        results=session.get("results"),
        sorted_allocations=session.get("sorted_allocations"),
        pairs=session.get("pairs"),
        threes=session.get("threes"),
        matrices_result=session.get("matrices_result"),
        ranges_result=session.get("ranges_result"),
        total_people=session.get("total_people", ""),
        people=session.get("people", ""),
        crews=session.get("crews", ""),
        zip=zip,
        enumerate=enumerate
    )

@app.route("/ranges", methods=["POST"])
def ranges():
    try:
        # Input parsing
        total_people_input = request.form.get("total_people", "").strip()
        total_people = int(total_people_input) if total_people_input else 0

        # Run ranges algorithm
        ranges_result = ranges(total_people)

        # Store the result in session
        session["ranges_result"] = ranges_result
        session["total_people"] = total_people

    except Exception as e:
        logging.error(f"Exception occurred while running ranges: {e}")
        logging.error(traceback.format_exc())
        return render_template(
            "index.html",
            error_message=f"An error occurred while running ranges: {e}",
            vehlist=",".join(map(str, session.get("vehlist", []))),
            pers5=session.get("pers5", ""),
            pers6=session.get("pers6", ""),
            pers7=session.get("pers7", ""),
            results=session.get("results"),
            sorted_allocations=session.get("sorted_allocations"),
            pairs=session.get("pairs"),
            threes=session.get("threes"),
            matrices_result=session.get("matrices_result"),
            ranges_result=None,
            total_people=total_people_input,
            people=session.get("people", ""),
            crews=session.get("crews", ""),
            zip=zip,
            enumerate=enumerate
        )

    return render_template(
        "index.html",
        vehlist=",".join(map(str, session.get("vehlist", []))),
        pers5=session.get("pers5", ""),
        pers6=session.get("pers6", ""),
        pers7=session.get("pers7", ""),
        results=session.get("results"),
        sorted_allocations=session.get("sorted_allocations"),
        pairs=session.get("pairs"),
        threes=session.get("threes"),
        matrices_result=session.get("matrices_result"),
        ranges_result=session.get("ranges_result"),
        total_people=session.get("total_people", ""),
        people=session.get("people", ""),
        crews=session.get("crews", ""),
        zip=zip,
        enumerate=enumerate
    )

if __name__ == "__main__":
    app.run(debug=True)
