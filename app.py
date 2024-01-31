# Import dependencies -- reuse code others have given us.
# Code from https://github.com/DuncanJF/BuyBestBrands/blob/main/app.py
import sqlite3
import os
import json
from markupsafe import escape
import datetime
from flask import Flask, render_template, request, url_for, redirect, abort, g

app = Flask("app")
# The database configuration
# Code from https://github.com/DuncanJF/BuyBestBrands/blob/main/app.py
DATABASE = os.environ.get("FLASK_DATABASE", "dining.db")


# Functions to help connect to the database
# And clean up when this application ends.
# Code from https://github.com/DuncanJF/BuyBestBrands/blob/main/app.py
def get_db_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db 

# Landing screen
# Main functionalities as facilities recommendation, popular, filter by type, and search filter
@app.route("/facilities-landing", methods=("GET", "POST"))
def facilities_landing():
    # call connect database function
    conn = get_db_connection()
    # incase that use tap on find after apply the search filter

    if request.method == "POST":
        # type for returning to inform frontend to display "All Type" on the list screen
        type = "all"

        # this query parameter (is_student_union) set as a default value for "none" dropdown
        is_student_union = "99"

        # input from frontend dropdown (main.html)
        number_of_guest = int(request.form['number-of-guest'])
        open_day = request.form['open-day']
        open_time = int(request.form['open-time'])

        # define variable which will apply on each search filter level
        result_after_guest=[]
        result_after_type=[]
        result_after_type_dup_validation = {}
        result_after_type_stage = []

        # final_result as a list of tuple that return the result list to frontend
        final_result = []
        # query list of dinning facilities from tbl_dining_profile and tbl_dining_type_mapping which joined by profile_id
        filter_list = conn.execute("SELECT tbl_dining_profile.profile_id, name, short_description, picture, type_id, open_day_time_list, number_of_guest, is_student_union, location FROM tbl_dining_profile RIGHT JOIN tbl_dining_type_mapping ON tbl_dining_profile.profile_id = tbl_dining_type_mapping.profile_id").fetchall()
        
        # filter number of guest (first query parameter)     
        if number_of_guest != 99:
            result_after_guest = [i for i in filter_list if i[6] == number_of_guest]
        else:
            result_after_guest = filter_list

        #remove duplication in case 1 profile_id have multiple type_id
        for i in result_after_guest:
            if i[0] not in result_after_type_dup_validation:
                result_after_type_stage.append(i)
                result_after_type_dup_validation[i[0]] = True
        result_after_type = result_after_type_stage

        # filter open day date (second and third query parameter)
        if open_day != "99":
            for i in result_after_type:
                if open_day in json.loads(i[5]):
                    if open_time != 99:
                        day_date_dict = json.loads(i[5])
                        if day_date_dict[open_day][0] <= open_time <= day_date_dict[open_day][1]:
                                final_result.append(i)
                    else:
                        final_result.append(i)
        else:
            final_result = result_after_type
        conn.close()

        # for webpage result to render list screen with applyed search filter
        return render_template("list.html",dining_type = type, pre_select_guest = number_of_guest, pre_select_day = open_day, pre_select_time = open_time, pre_su = is_student_union, details = final_result)

    else:
    # connect to database and query data from table
        boolean_value = "True"
        # query list of recommend dining facilities
        recommend_result = conn.execute("SELECT profile_id, name, picture FROM tbl_dining_profile WHERE is_recommend = ?",(boolean_value,)).fetchall()
        # query list of popular dining facilities
        popular_result = conn.execute("SELECT profile_id, name, picture, is_food_popular FROM tbl_dining_profile WHERE is_popular = ?",(boolean_value,)).fetchall()
        # query list of dining facilities type
        type_list = conn.execute("SELECT type_id, type_name FROM tbl_dining_type").fetchall()
        conn.close()
        return render_template("main.html",recommends = recommend_result, populars = popular_result, types = type_list)

# Facilities list screen
# Main functionalities as filter
@app.route("/facilities-list/<int:number_of_guest>/<string:open_day>/<int:open_time>/<string:is_student_union>/<int:type_id>",methods=("GET", "POST"))
def facilities_list(number_of_guest,open_day,open_time,is_student_union,type_id):

    # connect to database and query data from table
    conn = get_db_connection()

    # most of the following path similar to landing screen but add the parameter related to is_student_union which filter facilities that owned by Warwick student union
    type = conn.execute("SELECT type_name FROM tbl_dining_type WHERE type_id = ?",(type_id,)).fetchall()
    result_after_guest=[]
    result_after_type=[]
    result_after_type_dup_validation = {}
    result_after_type_stage = []
    result_after_time = []
    final_result = []
    filter_list = conn.execute("SELECT tbl_dining_profile.profile_id, name, short_description, picture, type_id, open_day_time_list, number_of_guest, is_student_union, location FROM tbl_dining_profile RIGHT JOIN tbl_dining_type_mapping ON tbl_dining_profile.profile_id = tbl_dining_type_mapping.profile_id").fetchall()
    
    # set parameter in case that use tab on "Find" button 
    if request.method == "POST":  
        number_of_guest = int(request.form['number-of-guest'])
        open_day = request.form['open-day']
        open_time = int(request.form['open-time'])
        is_student_union = request.form['student-union']


    # filter number of guest (first query parameter)     
    if number_of_guest != 99:
        result_after_guest = [i for i in filter_list if i[6] == number_of_guest]
    else:
        result_after_guest = filter_list

    # filter type (fifth query parameter)
    if type_id != 99:
        result_after_type = [i for i in result_after_guest if i[4] == type_id]
        type = type[0][0]
    else:
        type = "all"
        #remove duplication in case that one profile_id have multiple type_id
        for i in result_after_guest:
            if i[0] not in result_after_type_dup_validation:
                result_after_type_stage.append(i)
                result_after_type_dup_validation[i[0]] = True
        result_after_type = result_after_type_stage

    # filter open day date (second and third query parameter)
    if open_day != "99":
        for i in result_after_type:
            # apply json that the data on the table store as text of dictionary to transform to dict type to perform python logic
            if open_day in json.loads(i[5]):
                if open_time != 99:
                    day_date_dict = json.loads(i[5])
                    # check that open time within open time
                    if day_date_dict[open_day][0] <= open_time <= day_date_dict[open_day][1]:
                            result_after_time.append(i)
                else:
                    result_after_time.append(i)
    else:
        result_after_time = result_after_type

    # filter student union (fourth query parameter)
    if is_student_union != "99":
        for i in result_after_time:
            if is_student_union == i[7]:
                final_result.append(i)
    else:
        final_result = result_after_time
    conn.close()

    # for rendering list.html webpage
    return render_template("list.html",dining_type = type, pre_select_guest = number_of_guest, pre_select_day = open_day, pre_select_time = open_time, pre_su = is_student_union, details = final_result)

# Facilities details screen
# Main functionalities as display detail of each facilities
# This route also include "POST" method for submit customer review
@app.route("/facilities-detail/<int:profile_id>", methods=("GET", "POST"))
def facilities_detail(profile_id):

    # connect to database and query data from table
    conn = get_db_connection()
    
    # For Future implementation : customer review feature
    if request.method == "POST":
            insert_supps = conn.execute(
                "INSERT INTO tbl_customer_review (profile_id, name, description, rating) VALUES (?,?,?,?)",
                (
                    profile_id,
                    request.form['username'],
                    request.form['description'],
                    request.form['rating'],
                ),
            )
            conn.commit()
    
    # for retrieve list of detail config by profile_id
    supps = conn.execute("SELECT * FROM tbl_dining_profile WHERE profile_id = ?",(profile_id,)).fetchall()

    # for retrieve the customer review information
    reviews = conn.execute("SELECT * FROM tbl_customer_review WHERE profile_id = ?",(profile_id,)).fetchall()

    # logic for calculate the average rating on each profile_id
    # also handle the case where divided by zero
    sum = 0
    if len(reviews) != 0:
        number = len(reviews)
        for i in reviews:
            sum += i[4]
        average_rating = round(sum/number,2)
    else:
        average_rating = 0
    conn.close()
    return render_template("detail.html", details = supps, reviews = reviews, average_rating = average_rating)

if __name__ == "__main__":
    app.run(debug=True)




