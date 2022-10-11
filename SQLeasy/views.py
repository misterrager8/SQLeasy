from flask import current_app, redirect, render_template, request, url_for

from SQLeasy.models import Database, Table


@current_app.route("/")
def index():
    return render_template("index.html", dbs=Database.all())


@current_app.route("/create_database", methods=["POST"])
def create_database():
    database_ = Database(request.form["name"])
    database_.create()

    return redirect(request.referrer)


@current_app.route("/create_table", methods=["POST"])
def create_table():
    table_ = Table(
        request.form["name"],
        Database(request.args.get("db")),
        request.form.getlist("cols"),
    )
    table_.create()

    return redirect(url_for("database", db=request.args.get("db")))


@current_app.route("/drop_table")
def drop_table():
    table_ = Table(request.args.get("table"), Database(request.args.get("db")))
    table_.drop()

    return redirect(request.referrer)


@current_app.route("/database")
def database():
    database_ = Database(request.args.get("db"))
    return render_template("database.html", database_=database_)


@current_app.route("/drop_database")
def drop_database():
    database_ = Database(request.args.get("db"))
    database_.drop()

    return redirect(url_for("index"))
