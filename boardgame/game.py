from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import board as boardmodule
from . import socketio
from boardgame.db import get_db

from flask_socketio import emit

from boardgame.colors import colors

from boardgame.db import get_db
bp = Blueprint('game', __name__)

from boardgame.player import get_players, get_player, update_player_money

@bp.route("/game")
def run_game():
    """"Serves game page"""
    return render_template("game.html", join_code = session["join_code"], nickname = session["nickname"], team_colors = colors);

@socketio.on('connect')
def connect():
    print("connected")
    join_code = session["join_code"]
    emit_board(join_code)

@socketio.on('start_game')
def start_game():
    print("starting!")
    join_code = session["join_code"]
    db = get_db()
    players = get_players(join_code)
    board = boardmodule.get_board(join_code)

    # Inserts starting position
    if(players["player1"] != None):
       boardmodule.set_square(join_code, 8, 8, players["player1"])
    if(players["player2"] != None):
       boardmodule.set_square(join_code, 12, 12, players["player2"])
    if(players["player3"] != None):
       boardmodule.set_square(join_code, 8, 12, players["player3"])
    if(players["player4"] != None):
       boardmodule.set_square(join_code, 12, 8, players["player4"])

    set_turn(join_code, 1)

    game_message("Game started! %s's turn" % players["player1"]["nickname"], join_code)
    emit_board(join_code)

@socketio.on('end_turn')
def end_turn():
    """Called when a player ends their turn"""
    join_code = session["join_code"]
    nickname = session["nickname"]
    players = get_players(join_code)

    increment_turn()

    game_message("Next Turn! %s's turn" % players["player" + str(turn)]["nickname"], join_code)



@socketio.on('make_move')
def move(data):
    print(str(data["i"]) + " " + str(data["j"]))
    if(session["player_num"] == get_turn()):
        if(get_player[nickname].money >= 100) {
            update_player_money(-100)
        }

    db = get_db()

def game_message(msg, join_code):
    emit('message', {"data":msg, "room":join_code}, broadcast = True)

def emit_board(join_code):
    emit('update_board', {"board":boardmodule.get_json_board(join_code),"room":join_code}, broadcast = True)
