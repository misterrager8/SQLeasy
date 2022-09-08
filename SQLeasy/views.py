from flask import current_app, redirect, render_template, request, url_for

from SQLeasy import cursor_
from SQLeasy.models import Database


@current_app.route("/")
def index():
    cursor_.execute("SHOW DATABASES")
    dbs = [Database(i[0]) for i in cursor_.fetchall()]
    return render_template("index.html", dbs=dbs)


@current_app.route("/create_database", methods=["POST"])
def create_database():
    database_ = Database(request.form["name"])
    cursor_.execute(f"CREATE DATABASE {database_.name}")

    return redirect(url_for("database", name=database_.name))


@current_app.route("/create_table", methods=["POST"])
def create_table():
    dbname = request.args.get("dbname")
    name = request.form["name"]
    cols = zip(request.form.getlist("col"), request.form.getlist("datatype"))

    cursor_.execute("USE %s" % dbname)
    cursor_.execute(
        "CREATE TABLE %s %s"
        % (name, "(" + ", ".join([(i[0] + " " + i[1]) for i in cols]) + ")")
    )

    return redirect(url_for("database", name=dbname))


@current_app.route("/drop_table")
def drop_table():
    dbname = request.args.get("dbname")
    tablename = request.args.get("tablename")

    cursor_.execute(f"USE {dbname}")
    cursor_.execute(f"DROP TABLE {tablename}")

    return redirect(request.referrer)


@current_app.route("/database")
def database():
    database_ = Database(request.args.get("name"))
    return render_template("database.html", database_=database_)


@current_app.route("/drop_database")
def drop_database():
    name = request.args.get("name")
    cursor_.execute(f"DROP DATABASE {name}")

    return redirect(url_for("index"))
