from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import time
from . import socketio
from flask_socketio import join_room, leave_room
from boardgame.db import get_db

from boardgame.emissions import *

from boardgame.colors import colors

from boardgame.db import get_db
bp = Blueprint('lobby', __name__)

from boardgame.player import *

from boardgame.turn import get_turn, set_turn, increment_turn

from boardgame.lobbydb import get_list, set_list, remove_list
@socketio.on('connect', namespace="/lobby")
def connect():
    join_code = session["join_code"]
    join_room(join_code)
    emit_message("%s joined the game!" % session["nickname"], join_code, channel="/lobby")
    emit_lobby(join_code, get_list(join_code))

@bp.route("/lobby", methods = ("GET","POST"))
def enter_lobby():
    return render_template("lobby.html", join_code = session["join_code"], nickname = session["nickname"])

@socketio.on('start_game', namespace="/lobby")
def start_game():
    join_code = session["join_code"]
    db = get_db()
    # Creates a row in player table
    db.execute(
                'INSERT INTO game (join_code) VALUES (?)', (join_code,)
            )
    db.commit()

    # Gets players from the lobby database
    players = get_list(join_code)
    # Creates board in the player database
    create_board(join_code)
    for i in range(len(players)):
        add_player(join_code, players[i])
    # Switches players list to full player objects
    players = get_players(join_code)

    # Inserts starting position
    if(players["player1"] != None):
       set_square(join_code, 1, 1, players["player1"])
    if(players["player2"] != None):
       set_square(join_code, 4,4 , players["player2"])
    if(players["player3"] != None):
       set_square(join_code, 1, 4, players["player3"])
    if(players["player4"] != None):
       set_square(join_code, 4, 1, players["player4"])

    # Removes row from lobby database
    remove_list(join_code)
    # set's turn to first player
    set_turn(join_code, 1)
    # Forces all connected sockets to call intermediate method, which
    # sets session variable and redirects them to game
    emit('redirect', {'url': url_for('lobby.intermediate')}, room = join_code, broadcast = True)


@bp.route("/intermediate", methods = ["GET"])
def intermediate():
    num = get_num_player(session["join_code"], session["nickname"])
    session["player_num"] = num
    return redirect(url_for('game.run_game'))

@socketio.on('disconnect', namespace="/lobby")
def disconnect():
    leave_room(join_code)
    join_code = session["join_code"]
    emit_message("%s left the game..." % session["nickname"], session["join_code"])
    # If player is last one, removes lobby from DB
    players = get_list(join_code)
    if players == None:
        # list has already been removed or doesn't exist
        return
    players.remove(session["nickname"])

    if len(players) == 0:
        remove_list(join_code)
    else:
        set_list(join_code, players)
        emit_lobby(join_code, get_list(join_code))
