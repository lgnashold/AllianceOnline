COLOR1 = "#FF00FF"
COLOR2 = "#0000FF"
COLOR3 = "#FF00FF"
COLOR4 = "#FF0000"
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import board
from . import socketio
from boardgame.db import get_db

from flask_socketio import emit

from boardgame.db import get_db
bp = Blueprint('game', __name__)

@bp.route("/game")
def run_game():
    """"Serves game page"""
    return render_template("game.html", join_code = session["join_code"], nickname = session["nickname"]);

@socketio.on('connect')
def connect():
    print("connected")
    join_code = session["join_code"]
    emit('update_board', {"board":board.get_json_board(join_code),"room":join_code}, broadcast = True)

@socketio.on('startgame')
def startgame():
    join_code = session["join_code"]
    db = get_db()

    game = db.execute(
            "SELECT * FROM game WHERE join_code = (?)", (join_code,)
    ).fetchone()

    board = game.get_board()

    if(game["player1"] != None):
        board[8][8]["color"] = COLOR1


@socketio.on('move')
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    db = get_db()

def game_message(msg, join_code):
    emit('message', {"data":msg, "room":join_code}, broadcast = True)
