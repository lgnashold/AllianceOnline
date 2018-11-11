from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from boardgame.board import *
from . import socketio
from boardgame.db import get_db

from boardgame.emissions import *

from flask_socketio import emit

from boardgame.colors import colors

from boardgame.db import get_db
bp = Blueprint('game', __name__)

from boardgame.player import *

from boardgame.turn import get_turn, set_turn, increment_turn

import json

@bp.route("/game")
def run_game():
    """"Serves game page"""
    return render_template("game.html", join_code = session["join_code"], nickname = session["nickname"], team_colors = colors);

@socketio.on('connect')
def connect():
    print("connected")
    join_code = session["join_code"]
    emit_board(join_code)
    emit_message("%s joined the game!" % session["nickname"], join_code)
    flash("Test Flash")

@socketio.on('end_turn')
def end_turn():
    """Called when a player ends their turn"""
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    players = get_players(join_code)
    turn = get_turn(join_code)

    if turn == player_num:
        increment_turn(join_code)
        emit_message("Next Turn! %s's turn" % players["player" + str(turn)]["nickname"], join_code)
        # sums total spaces on board controlled by a player
        spaces = 0
        board = get_board(join_code)
        for row in board:
            for space in row:
                if space["name"] == nickname:
                    spaces += 1
        money = spaces * 50
        update_player_money(join_code, player_num, money)
    elif turn != None:
        emit_message("It is not your turn, it is %s's turn" % players["player" + str(turn)]["nickname"], join_code)
    else:
        emit_message("Game has not started yet")

@socketio.on('disconnect')
def disconnect():
    emit_message("%s left the game..." % session["nickname"], session["join_code"])
    remove_player(session["join_code"],session["player_num"])
    check_empty(session["join_code"])


@socketio.on('make_move')
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    player = get_player(join_code, player_num)
    i = data['i']
    j = data['j']

    if player_num == get_turn(join_code) :
        cost = check_connected(join_code, i, j, None)
        # if cost is -1, then no player controls square
        if cost == -1:
            cost = 100
        else:
            # Otherwise does 30 times num of connected squares
            cost = cost * 30
        if player["money"] >= cost :
            errormsg = set_square(join_code, i, j, player, player_initiated=True)
            if(errormsg == None):
                update_player_money(join_code, player_num, -1 * cost)
                remove_no_territory(join_code)
                emit_message("Player %s took a square!" % nickname, join_code)
                emit_board(join_code)
            else:
                emit_message(errormsg, join_code)
                print(errormsg)
        else:
            emit_message("You do not have enough money", join_code)
    elif get_turn(join_code) != None:
        emit_message("It is not your turn", join_code)
    else:
        emit_message("Game has not started yet", join_code)


@socketio.on('change_team')
def change_team(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    team = data["team"]
    player = get_player(join_code, player_num)

    if player_num == get_turn(join_code):
        if player["money"] >= 50 and num_players_on_team(join_code, team) < 2:
            update_player_money(join_code, player_num, -50)
            update_player_team(join_code, player_num, team)
            emit_message("Player {0} changed to {1}!".format(nickname, team), join_code)
            emit_board(join_code)
            print("Emitted")
        else:
            emit_message("You do not have enough money to change teams", join_code)
    elif (get_turn(join_code) != None):
        emit_message("It is not your turn", join_code)

def remove_no_territory(join_code):
    board = get_board(join_code)

    player1 = False
    player2 = False
    player3 = False
    player4 = False

    players = get_players(join_code)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if (get_num_player(join_code,board[row][col]["name"]) == 1):
                player1 = True
            elif (get_num_player(join_code,board[row][col]["name"]) == 2):
                player2 = True
            elif (get_num_player(join_code,board[row][col]["name"]) == 3):
                player3 = True
            elif (get_num_player(join_code,board[row][col]["name"]) == 4):
                player4 = True

    if(not player1):
        remove_player(join_code,1)
    if(not player2):
        remove_player(join_code,2)
    if(not player3):
        remove_player(join_code,3)
    if(not player4):
        remove_player(join_code,4)

def check_empty(join_code):
    db = get_db()
    players = get_players(join_code)
    count = 0
    for key,value in players.items():
        if players[key] != None:
            count+=1

    if (count < 1):
        db.execute("DELETE FROM game WHERE join_code = (?)",(join_code,))
        db.commit()
