import click

from SQLeasy import config, create_app, cursor_
from SQLeasy.models import Database

app = create_app(config)


@click.group()
def cli():
    """SQLEasy CLI"""
    pass


@cli.command()
@click.argument("name")
def create_db(name):
    """Create a db"""
    cursor_.execute(f"CREATE DATABASE {name}")
    click.secho(f"Database: {name} created.", fg="cyan")


@cli.command()
def list_dbs():
    """List dbs"""
    cursor_.execute("SHOW DATABASES")
    results = [Database(i[0]) for i in cursor_.fetchall()]
    for i in results:
        click.secho(f"{i.name} ({len(i.show_tables())} table(s))", fg="cyan")


@cli.command()
@click.argument("name")
def show_tables(name):
    """Show tables in db"""
    for i in Database(name).show_tables():
        click.secho(f"\nTABLE: {i.name}")
        for j in i.describe():
            click.secho(j, fg="cyan")


@cli.command()
@click.argument("name")
def drop_db(name):
    """Delete a db"""
    cursor_.execute(f"DROP DATABASE {name}")
    click.secho(f"Database: {name} deleted.", fg="cyan")


@cli.command()
def web():
    """Web UI"""
    app.run()
