from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import socketio
from boardgame.db import get_db

from boardgame.emissions import *

from boardgame.colors import colors

from boardgame.db import get_db
bp = Blueprint('lobby', __name__)

from boardgame.player import *

from boardgame.turn import get_turn, set_turn, increment_turn

from boardgame.lobbydb import get_list, set_list
@socketio.on('connect', namespace="/lobby")
def connect():
    join_code = session["join_code"]
    print("EVENT: " + session["nickname"] + " joined the lobby with join code: " + join_code)
    emit_message("%s joined the game!" % session["nickname"], join_code, channel="/lobby")
    emit_lobby(join_code, get_list(join_code))

@bp.route("/lobby", methods = ("GET","POST"))
def enter_lobby():
    return render_template("lobby.html", join_code = session["join_code"], nickname = session["nickname"])

@socketio.on('start_game', namespace="/lobby")
def start_game():
    join_code = session["join_code"]
    db = get_db()
    players = get_players(join_code)
    board = get_board(join_code)

    
    if get_turn(join_code) != None:
        return
    # Inserts starting position
    if(players["player1"] != None):
       set_square(join_code, 1, 1, players["player1"])
    if(players["player2"] != None):
       set_square(join_code, 4,4 , players["player2"])
    if(players["player3"] != None):
       set_square(join_code, 1, 4, players["player3"])
    if(players["player4"] != None):
       set_square(join_code, 4, 1, players["player4"])

    set_turn(join_code, 1)

    emit_message("Game started! %s's turn" % players["player1"]["nickname"], join_code)
    # emit_money(join_code,get_players(join_code))
    emit_board(join_code)
    emit('redirect', {'url': url_for('game.run_game')}, broadcast = True)

@socketio.on('disconnect', namespace="/lobby")
def disconnect():
    join_code = session["join_code"]
    emit_message("%s left the game..." % session["nickname"], session["join_code"])
    print("LOBBY DISCONNECT")
    players = get_list(join_code)
    players.remove(session["nickname"])
    set_list(join_code, players)
    emit_lobby(join_code, get_list(join_code))
