from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from boardgame.board import *
from . import socketio
from boardgame.db import get_db

from boardgame.emissions import emit_message, emit_board 

from flask_socketio import emit

from boardgame.colors import colors

from boardgame.db import get_db
bp = Blueprint('game', __name__)

from boardgame.player import get_players, get_player, update_player_money

from boardgame.turn import get_turn, set_turn, increment_turn

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
    board = get_board(join_code)

    # Inserts starting position
    if(players["player1"] != None):
       set_square(join_code, 8, 8, players["player1"])
    if(players["player2"] != None):
       set_square(join_code, 12, 12, players["player2"])
    if(players["player3"] != None):
       set_square(join_code, 8, 12, players["player3"])
    if(players["player4"] != None):
       set_square(join_code, 12, 8, players["player4"])

    set_turn(join_code, 1)

    emit_message("Game started! %s's turn" % players["player1"]["nickname"], join_code)
    emit_board(join_code)

@socketio.on('end_turn')
def end_turn():
    """Called when a player ends their turn"""
    join_code = session["join_code"]
    nickname = session["nickname"]
    players = get_players(join_code)

    increment_turn()

    emit_message("Next Turn! %s's turn" % players["player" + str(turn)]["nickname"], join_code)



@socketio.on('make_move')
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    player = get_player(join_code, player_num)
    i = data['i']
    j = data['j']

    if player_num == get_turn(join_code) :
        if player["money"] >= 100 :
            update_player_money(join_code, player_num, -100)
            set_square(join_code, i, j, player)
            emit_message("Player %s took a square!" % nickname, join_code)
            emit_board(join_code)
