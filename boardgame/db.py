import sqlite3

import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Returns the db being used"""
    # Database is stored in g
    # Makes sure it doesn't create duplicate connections
    if 'db' not in g:
        g.db = sqlite3.connect(
                # Location of database is stored in app's config file
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """The function that starts the database from schema file"""
    db = get_db()
    # Opens file from schema.sql with error checking
    with current_app.open_resource('schema.sql') as f:
        # Executes the file f as a sql script
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """"Clear the existing cache and create new tables"""
    init_db()
    click.echo("Initialised the database.")

def init_app(app):
    # Adds close_db to functions called when app is closed
    app.teardown_appcontext(close_db)
    # Addds click command to flask
    app.cli.add_command(init_db_command)
