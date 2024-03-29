import os
import webbrowser

import click
import dotenv
import mysql.connector
from flask import Flask, Response, render_template, request

# CONFIG

dotenv.load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
FG_COLOR = os.getenv("fg_color") or "blue"

# INIT

mysql_ = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST)
cursor_ = mysql_.cursor()

app = Flask(
    __name__, template_folder="webview/templates", static_folder="webview/static"
)


# MODELS


class Database(object):
    def __init__(self, name: str):
        self.name = name

    @property
    def tables(self) -> list:
        cursor_.execute(f"USE {self.name}")
        cursor_.execute("SHOW TABLES")
        return [Table(self.name, i[0]) for i in cursor_.fetchall()]

    @classmethod
    def all(cls) -> list:
        cursor_.execute("SHOW DATABASES")
        return [Database(i[0]) for i in cursor_.fetchall()]

    def create(self):
        cursor_.execute(f"CREATE DATABASE IF NOT EXISTS {self.name}")

    def drop(self):
        cursor_.execute(f"DROP DATABASE {self.name}")

    def to_dict(self):
        return dict(name=self.name, tables=[i.name for i in self.tables])


class Table(object):
    def __init__(self, database: str, name: str):
        self.database = database
        self.name = name

    def create(self, columns: list = []):
        cols = ", ".join([f"{i.name} {i.type.upper()}" for i in columns])
        cursor_.execute(
            f"CREATE TABLE IF NOT EXISTS {self.database}.{self.name} (id INT PRIMARY KEY AUTO_INCREMENT{(', ' + cols) if len(columns) != 0 else ''})"
        )

    def truncate(self):
        cursor_.execute(f"TRUNCATE TABLE {self.database}.{self.name}")

    def drop(self):
        cursor_.execute(f"DROP TABLE {self.database}.{self.name}")

    @property
    def columns(self) -> list:
        cursor_.execute(f"DESCRIBE {self.database}.{self.name}")

        return [
            Column(i[0], type_=i[1].decode(), primary_key=i[3] == "PRI")
            for i in cursor_.fetchall()
        ]

    @property
    def description(self) -> str:
        return "\n".join(
            [
                f"{i.name} {i.type.upper()}{' PRIMARY KEY' if i.primary_key else ''}"
                for i in self.columns
            ]
        )

    def to_dict(self):
        return dict(name=self.name, columns=[i.to_dict() for i in self.columns])


class Column(object):
    def __init__(
        self,
        name: str,
        type_: str = None,
        null=None,
        primary_key=None,
        default=None,
        extra=None,
    ):
        self.name = name
        self.type = type_
        self.null = null
        self.primary_key = primary_key
        self.default = default
        self.extra = extra

    def add(self, database, table):
        cursor_.execute(f"ALTER TABLE {database}.{table} ADD {self.name} {self.type}")

    def drop(self, database, table):
        cursor_.execute(f"ALTER TABLE {database}.{table} DROP COLUMN {self.name}")

    def change_type(self, database, table, new_type):
        cursor_.execute(
            f"ALTER TABLE {database}.{table} MODIFY COLUMN {self.name} {new_type}"
        )

    def to_dict(self):
        return dict(name=self.name, type_=self.type)


# MAIN


@click.group()
def cli():
    """SQLeasy command-line interface."""
    pass


@cli.command()
def show_dbs():
    """Show all databases."""
    click.secho("\n".join([i.name for i in Database.all()]), fg=FG_COLOR)


@cli.command()
@click.option("-n", "--name", prompt=True)
def create_db(name):
    """Create a new database."""
    Database(name).create()

    click.secho(f"{name} database created.", fg=FG_COLOR)


@cli.command()
@click.option("-n", "--name", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def drop_db(name):
    """Delete a database."""
    Database(name).drop()

    click.secho(f"{name} database dropped.", fg=FG_COLOR)


@cli.command()
@click.option("-d", "--db", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def create_table(db):
    """Create a new table."""
    Table(db, click.prompt(f"CREATE TABLE FOR {db}")).create()

    click.secho(f"Table created for {db}.", fg=FG_COLOR)


@cli.command()
@click.option("-n", "--name", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def show_tables(name):
    """Show tables in the selected database."""
    click.secho("\n".join([i.name for i in Database(name).tables]), fg=FG_COLOR)


@cli.command()
@click.option("-d", "--db", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def describe_table(db):
    """Show description of a selected table."""
    database_ = Database(db)
    table_ = Table(
        database_.name,
        click.prompt("\n".join([i.name for i in database_.tables]) + "\n"),
    )
    click.secho(table_.description, fg=FG_COLOR)


@cli.command()
@click.option("-d", "--db", prompt="\n".join([i.name for i in Database.all()]) + "\n")
@click.option(
    "-a", "--action", prompt=True, type=click.Choice(["add", "change-type", "drop"])
)
def alter_table(db, action):
    """Alter a selected table with the selected action."""
    database_ = Database(db)
    table_ = Table(
        database_.name,
        click.prompt("\n".join([i.name for i in database_.tables]) + "\n"),
    )

    if action == "add":
        Column(click.prompt("column name"), type_=click.prompt("type")).add(
            db, table_.name
        )
    elif action == "drop":
        Column(click.prompt("\n".join([i.name for i in table_.columns]))).drop(
            db, table_.name
        )
    elif action == "change-type":
        Column(click.prompt("\n".join([i.name for i in table_.columns]))).change_type(
            db, table_.name, click.prompt("new datatype")
        )

    click.secho(f"Table altered.", fg=FG_COLOR)


@cli.command()
@click.option("-d", "--db", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def truncate(db):
    """Clear a selected table of all data."""
    database_ = Database(db)
    table_ = Table(
        database_.name,
        click.prompt("\n".join([i.name for i in database_.tables]) + "\n"),
    )
    table_.truncate()

    click.secho(f"Table truncated.", fg=FG_COLOR)


@cli.command()
@click.option("-d", "--db", prompt="\n".join([i.name for i in Database.all()]) + "\n")
def drop_table(db):
    """Drop a selected table."""
    database_ = Database(db)
    table_ = Table(
        database_.name,
        click.prompt("\n".join([i.name for i in database_.tables]) + "\n"),
    )
    table_.drop()

    click.secho(f"Table dropped from {db}.", fg=FG_COLOR)


@cli.command()
@click.option("-d", "--debug", is_flag=True)
def web(debug):
    """Launch web interface."""
    if not debug:
        webbrowser.open("http://localhost:5000")
    app.run(debug=debug)


# API


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/show_dbs")
def show_dbs():
    return dict(dbs=[i.name for i in Database.all()])


@app.post("/create_database")
def create_database():
    database_ = Database(request.form.get("name"))
    database_.create()

    return database_.to_dict()


@app.get("/get_database")
def get_database():
    return Database(request.args.get("name")).to_dict()


@app.get("/delete_database")
def delete_database():
    database_ = Database(request.args.get("name"))
    database_.drop()

    return Response(status=200)


@app.post("/create_table")
def create_table():
    table_ = Table(request.form.get("database"), request.form.get("name"))
    table_.create()

    return table_.to_dict()


@app.get("/get_table")
def get_table():
    return Table(request.args.get("database"), request.args.get("name")).to_dict()


@app.get("/delete_table")
def delete_table():
    table_ = Table(request.args.get("database"), request.args.get("name"))
    table_.drop()

    return Response(status=200)


@app.post("/create_column")
def create_column():
    Column(request.form.get("name"), type_=request.form.get("type_")).add(
        request.form.get("database"), request.form.get("table")
    )

    return Response(status=200)


@app.get("/delete_column")
def delete_column():
    Column(request.args.get("name")).drop(
        request.args.get("database"), request.args.get("table")
    )

    return Response(status=200)
