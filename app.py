# Import dependencies -- reuse code others have given us.
import sqlite3
import os
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

#@app.route("/index_v2/<int:profile_id>")
#def index_v2(profile_id):
#    conn = get_db_connection()
#    supps = conn.execute("SELECT * FROM tbl_dining_profile WHERE profile_id = ?",(profile_id,)).fetchall()
#    conn.close()
#    return "<h1>{}</h1>".format(supps[0][:5])

@app.route("/facilities-detail/<int:profile_id>")
def facilities_detail(profile_id):
    conn = get_db_connection()
    supps = conn.execute("SELECT * FROM tbl_dining_profile WHERE profile_id = ?",(profile_id,)).fetchall()
    conn.close()
    return render_template("detail.html", details = supps)

if __name__ == "__main__":
    app.run(debug=True)

