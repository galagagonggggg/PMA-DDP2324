# Import dependencies -- reuse code others have given us.
import sqlite3
import os
import json
from markupsafe import escape
import datetime
from flask import Flask, render_template, request, url_for, redirect, abort, g

app = Flask("app")

# The database configuration
DATABASE = os.environ.get("FLASK_DATABASE", "dining.db")


# Functions to help connect to the database
# And clean up when this application ends.
def get_db_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Each @app.route(...) indicates a URL.
# Using that URL causes the function immediately after the @app.route(...) line to run.
@app.route("/")
@app.route("/index/")
def hello():
    """Return some friendly text."""
    return "Hello, World!"

@app.route("/index_v2/<int:profile_id>")
def index_v2(profile_id):
    conn = get_db_connection()
    supps = conn.execute("SELECT * FROM tbl_dining_profile").fetchall()
    conn.close()
    return "<h1>{}</h1>".format(supps)

@app.route("/facilities-list/<int:number_of_guest>/<string:open_day>/<int:open_time>/<string:is_student_union>/<int:type_id>",methods=("GET", "POST"))
def facilities_list(number_of_guest,open_day,open_time,is_student_union,type_id):
    #if request.method == "POST":
    #    conn = get_db_connection()
    #    supps = conn.execute(
    #        "INSERT INTO products VALUES (?,?,?,?,?,?,?,?)",
    #        (
    #            request.form["product_id"],
    #            request.form["supplier_id"],
    #            request.form["quantity"],
    #            request.form["short_description"],
    #            request.form["long_description"],
    #            request.form["minimum_age"],
    #            request.form["input_unit_price"],
    #            request.form["shopper_unit_price"],
    #        ),
    #    )
    #    conn.commit()
    #    conn.close()
    #    return redirect(url_for("products"))
    conn = get_db_connection()
    type = conn.execute("SELECT type_name FROM tbl_dining_type WHERE type_id = ?",(type_id,)).fetchall()
    result_after_guest=[]
    result_after_type=[]
    result_after_type_dup_validation = {}
    result_after_type_stage = []
    result_after_time = []
    final_result = []
    filter_list = conn.execute("SELECT tbl_dining_profile.profile_id, name, short_description, picture, type_id, open_day_time_list, number_of_guest, is_student_union, location FROM tbl_dining_profile RIGHT JOIN tbl_dining_type_mapping ON tbl_dining_profile.profile_id = tbl_dining_type_mapping.profile_id").fetchall()
    if number_of_guest != 99:
        result_after_guest = [i for i in filter_list if i[6] == number_of_guest]
    else:
        result_after_guest = filter_list

    if type_id != 99:
        result_after_type = [i for i in result_after_guest if i[4] == type_id]
        type = type[0][0]
    else:
        type = "all"
        #remove duplication in case 1 profile_id have multiple type_id
        for i in result_after_guest:
            if i[0] not in result_after_type_dup_validation:
                result_after_type_stage.append(i)
                result_after_type_dup_validation[i[0]] = True
        result_after_type = result_after_type_stage

    if open_day != "99":
        for i in result_after_type:
            if open_day in json.loads(i[5]):
                if open_time != 99:
                    day_date_dict = json.loads(i[5])
                    if day_date_dict[open_day][0] <= open_time <= day_date_dict[open_day][1]:
                            result_after_time.append(i)
                else:
                    result_after_time.append(i)
    else:
        result_after_time = result_after_type

    if is_student_union != "99":
        for i in result_after_time:
            if is_student_union == i[7]:
                final_result.append(i)
    else:
        final_result = result_after_time
    conn.close()
    #for production webpage
    #return render_template("list.html",dining_type = type, pre_select_guest = number_of_guest, pre_select_day = open_day, pre_select_time = open_time, pre_su = is_student_union)
    
    #trail for result from each variable
    return "<h1>{}</h1>".format(final_result)

@app.route("/facilities-detail/<int:profile_id>")
def facilities_detail(profile_id):
    conn = get_db_connection()
    supps = conn.execute("SELECT * FROM tbl_dining_profile WHERE profile_id = ?",(profile_id,)).fetchall()
    conn.close()
    return render_template("detail.html", details = supps)

if __name__ == "__main__":
    app.run(debug=True)


