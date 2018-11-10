import os

from flask import Flask

def create_app():
    # Creates an app
    # Instance relative config means paths in config files are relative to instance folder
    app = flask(__name__, instance_relative_config=True)
    
    # Edits configurations
    app.config["SECRET_KEY"] = "123kxjq0kx2rehxj"
    # instance_path is the instance folder
    app.config["DATABASE"] = os.path.join(app.instance_path, "boardgame.sqlite")
    
    # Insure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Test
    @app.route('/hello')
    def hello():
        return "Hello World"
