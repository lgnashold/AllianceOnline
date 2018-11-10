COLOR1 = "#FF00FF"
COLOR2 = "#0000FF"
COLOR3 = "#FF00FF"
COLOR4 = "#FF0000"
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import board as boardmodule
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
    emit_board(join_code)
@socketio.on('startgame')
def start_game():
    join_code = session["join_code"]
    db = get_db()
    game = get_game(join_code)
    board = boardmodule.get_board(join_code)

    # Inserts starting position
    if(game["player1"] != None):
        board[8][8]["color"] = COLOR1
    if(game["player2"] != None):
        board[12][12]["color"] = COLOR2

    # Sets turn
    db.execute(
            "UPDATE game SET turn = (?) WHERE join_code = (?)", (game["player1"], join_code)
    )
    db.commit()
    board.update_board(join_code)

    game_message("Game started! %s's turn" % game["player1"], join_code)
    emit_board(join_code)

@socketio.on('end_turn')
def end_turn():
    join_code = session["join_code"]
    nickname = session["nickname"]
    game = get_game(join_code)

@socketio.on('move')
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    db = get_db()

def get_game(join_code):
    game = db.execute(
            "SELECT * FROM game WHERE join_code = (?)", (join_code,)
    ).fetchone()
    return game

def game_message(msg, join_code):
    emit('message', {"data":msg, "room":join_code}, broadcast = True)

def emit_board(join_code):
    emit('update_board', {"board":boardmodule.get_json_board(join_code),"room":join_code}, broadcast = True)
