import os

from flask import Flask
from flask_socketio import SocketIO

# socketio is what you actually use
socketio = SocketIO()

def create_app():
    # Creates an app
    # Instance relative config means paths in config files are relative to instance folder
    app = Flask(__name__, instance_relative_config=True)

    # Edits configurations
    app.config["SECRET_KEY"] = "123kxjq0kx2rehxj"
    # instance_path is the instance folder
    app.config["DATABASE"] = os.path.join(app.instance_path, "boardgame.sqlite")
    app.config["COLORS"] = {"team1" : "#FF00FF", "team2":"#0000FF", "team3": "#FF00FF", "team4": "#FF0000"}
    # Insure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Test
    @app.route('/hello')
    def hello():
        return "Hello World"

    from . import board
    @app.route('/board')
    def boardinit():
         board.create_board("0")
         return "made board"

    # Initialises database, including registering init-db command
    from . import db
    db.init_app(app)

    from . import game
    app.register_blueprint(game.bp)

    from . import matchmaking
    app.register_blueprint(matchmaking.bp)

    socketio.init_app(app)

    # returns created app
    return app
