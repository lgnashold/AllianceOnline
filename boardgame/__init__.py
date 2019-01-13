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

    # Test
    @app.route('/hello')
    def hello():
        return "Hello World"

    # Initialises database, including registering init-db command
    from . import db
    db.init_app(app)

    from . import lobby
    app.register_blueprint(lobby.bp)

    '''
    from . import game
    app.register_blueprint(game.bp)
    '''
    
    from . import matchmaking
    app.register_blueprint(matchmaking.bp)

    socketio.init_app(app)

    # returns created app
    return app
