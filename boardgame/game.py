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

@bp.route("/game")
def run_game():
    """"Serves game page"""
    return render_template("game.html", join_code = session["join_code"], nickname = session["nickname"], team_colors = colors);

@bp.route("/lobby")
def enter_lobby():
        return render_template("lobby.html", join_code = session["join_code"], nickname = session["nickname"], team_colors = colors);

@socketio.on('connect')
def connect():
    print("connected")
    join_code = session["join_code"]
    emit_board(join_code)
    emit_message("%s joined the game!" % session["nickname"], join_code)


@socketio.on('start_game')
def start_game():
    print("starting!")
    join_code = session["join_code"]
    db = get_db()
    players = get_players(join_code)
    board = get_board(join_code)

    if get_turn(join_code) != None:
        return
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
    emit_money(join_code,get_players(join_code))
    emit_board(join_code)

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


@socketio.on('make_move')
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    player = get_player(join_code, player_num)
    i = data['i']
    j = data['j']

    if player_num == get_turn(join_code) :
        cost = check_connected(join_code, i, j, None) * 30
        # if cost is -1, then no player controls square
        if cost == -1:
            cost = 100 
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

    for row in range(len(board)):
        for col in range(len(board[row])):
            if (get_num_player(join_code,board[row][col]["nickname"]) == 1):
                player1 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 2):
                player2 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 3):
                player3 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 4):
                player4 = True

    if(not player1 and players.player1 != None):
        remove_player(1)
    if(not player2 and players.player2 != None):
        remove_player(2)
    if(not player3 and players.player3 != None):
        remove_player(3)
    if(not player4 and players.player4 != None):
        remove_player(4)
