import psycog2
import os
import urllib.parse as urlparse

import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Returns the db being used"""
    # Database is stored in g
    # Makes sure it doesn't create duplicate connections
    if 'db' not in g:
        # Gets the database URL
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        # Location of database is stored in app's config file
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        g["db"] = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
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
