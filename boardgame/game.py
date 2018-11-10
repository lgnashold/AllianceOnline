from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import board
from . import socketio

from flask_socketio import emit

from boardgame.db import get_db
bp = Blueprint('game', __name__)

@bp.route("/game")
def run_game():
    join_code = "0"
    #board.get_json_board(join_code)
    return render_template("game.html");

@socketio.on('connect')
def connect():
    emit('update_board', board.get_json_board(join_code), broadcast = True)
