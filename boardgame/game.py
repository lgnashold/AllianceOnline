from boardgame import matchmaking

COST_TEAM_SWITCH = 100
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from boardgame.board import *
from . import socketio
from boardgame.db import get_db

from boardgame.emissions import *

from flask_socketio import emit, join_room, leave_room

from boardgame.colors import colors

from boardgame.db import get_db

bp = Blueprint('game', __name__)

from boardgame.player import *

from boardgame.turn import get_turn, set_turn, increment_turn

from boardgame import connection_manager

import math

import json


@bp.route("/game")
def run_game():
    """"Serves game page"""
    if 'join_code' not in session:
        return redirect(url_for('matchmaking.index'))
    return render_template("game.html", join_code=session["join_code"], nickname=session["nickname"],
                           team_colors=colors);


@socketio.on('connect', namespace="/game")
def connect():
    print(f"{session['nickname']} CONNECTED TO {session['join_code']}")
    join_code = session["join_code"]
    join_room(join_code)
    emit_board(join_code)
    emit_money(join_code, get_players(join_code))
    emit_teams(join_code, colors, get_players(join_code))
    emit_message("%s joined the game!" % session["nickname"], join_code)
    player = get_player(join_code, get_turn(join_code))
    emit_turn(join_code, player["nickname"])
    player_num = get_num_player(join_code, session["nickname"])
    connection_manager.addPlayer(join_code, player_num)
    if test_end_game():
        emit_end_game(join_code, session["nickname"])


@socketio.on('disconnect', namespace="/game")
def disconnect():
    join_code = session["join_code"]
    player_num = get_num_player(join_code, session["nickname"])
    connection_manager.removePlayer(join_code, player_num)
    emit_message(f"{session['nickname']} left the game. {connection_manager.numberOfPlayers(join_code)} players left!",
                 join_code)

    # if player who quit is on their turn, increment turn
    if (str(get_turn(join_code)) == str(session["player_num"])):
        increment_turn(join_code)
        emit_turn(join_code, get_player(join_code, get_turn(join_code))["nickname"])

    # removes game if empty, otherwise deal with repairing the game
    check_empty(join_code)


# TODO: bug, player could have won here.


@socketio.on('end_turn', namespace="/game")
def end_turn():
    """Called when a player ends their turn"""
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    players = get_players(join_code)
    turn = get_turn(join_code)

    if turn == player_num:
        increment_turn(join_code)
        turn = get_turn(join_code)
        player = get_player(join_code, turn)

        # sums total spaces on board controlled by a player
        spaces = 0
        board = get_board(join_code)
        money = get_revenue(join_code, player["nickname"])
        update_player_money(join_code, turn, money)
        emit_turn(join_code, player["nickname"])


def split_teams(join_code):
    # checks if two final players are on same team, if so fixes that
    team = "none"
    count = 0
    if (get_num_players(join_code) == 2):
        count += 1
        players = get_players(join_code)
        for key, value in players.items():
            if value != None:
                if team == "none":
                    team = value["team"]
                else:
                    if team == value["team"]:
                        if (team == "team1"):
                            update_player_team(join_code, count, "team2")
                        else:
                            update_player_team(join_code, count, "team1")

        emit_board(join_code)
        check_empty(join_code)


def make_squares_empty(join_code, player_num):
    board = get_board(join_code)
    for row in range(BOARD_WIDTH):
        for col in range(BOARD_HEIGHT):
            if (board[row][col]["name"] == get_player(join_code, player_num)["nickname"]):
                board[row][col] = get_default_square()
    set_board(join_code, board)


def check_money(function, cost):
    """A wrapper function to avoid repeated code"""
    join_code = session["join_code"]
    player_num = session["player_num"]
    player = get_player(join_code, player_num)
    errormsg = None
    if player["money"] < cost:
        errormsg = "Not enough money"
    else:
        errormsg = function()
        if errormsg == None:
            update_player_money(join_code, player_num, -1 * cost)
            remove_no_territory(join_code)
            emit_board(join_code)
            if player["money"] - cost < get_min_cost():
                end_turn()
    if errormsg != None:
        emit_error(errormsg, join_code)


@socketio.on('make_move', namespace="/game")
def move(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    player = get_player(join_code, player_num)
    i = data['i']
    j = data['j']

    if player_num == get_turn(join_code):
        cost = get_cost_of_square(i, j)

        def make_move():
            errormsg = set_square(join_code, i, j, player, player_initiated=True)
            gameover = test_end_game()
            if gameover:
                emit_end_game(join_code, nickname)
            return errormsg

        check_money(make_move, cost)


@socketio.on('get_cost', namespace="/game")
def get_cost(data):
    print("GOT COST REQUEST")
    join_code = session["join_code"]
    i = data["i"]
    j = data["j"]
    player = get_player(join_code, session["player_num"])
    if (check_legal_move(join_code, i, j, player)):
        emit_cost(join_code, "#ffffff", get_cost_of_square(i, j), i, j)
    else:
        emit_cost(join_code, "#ff0000", get_cost_of_square(i, j), i, j)


@socketio.on('change_team', namespace="/game")
def change_team(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    team = data["team"]

    if player_num == get_turn(join_code):
        def change_team_inner():
            errormsg = None
            if num_players_on_team(join_code, team) >= math.ceil(get_num_players(join_code) / 2):
                errormsg = "There are already do many people on that team"
            else:
                update_player_team(join_code, player_num, team)
                emit_message("Player {0} changed to {1}!".format(nickname, team), join_code)
                emit_teams(join_code, colors, get_players(join_code))
            return errormsg

        check_money(change_team_inner, COST_TEAM_SWITCH)


def test_end_game():
    """Tests if the game is over, returns result"""
    join_code = session["join_code"]
    board = get_board(join_code)
    names = []
    for row in board:
        for col in row:
            space = col["name"]
            if space != None and space not in names:
                names.append(space)
    if (len(names) <= 1):
        return True
    return False


def check_empty(join_code):
    db = get_db()
    if connection_manager.numberOfPlayers(join_code) < 1:
        print("GAME EMPTY - DELETING: " + join_code)
        db.execute("DELETE FROM game WHERE join_code = (%s)", (join_code,))
        return True
    return False


# check if a move is legal
# TODO: very repetitive, since split up and used in move function, but not actually used there
def check_legal_move(join_code, i, j, player):
    board = get_board(join_code)
    new_color = colors[player["team"]]
    old_color = board[i][j]["color"]
    if (new_color == old_color):
        return False
    if (check_connected(join_code, i, j, new_color) < 1):
        return False
    if (player["money"] < get_cost_of_square(i, j)):
        return False
    return True


def remove_no_territory(join_code):
    print("REMOVING PLAYERS WITH NO TERRITORY")
    board = get_board(join_code)

    player1 = False
    player2 = False
    player3 = False
    player4 = False

    players = get_players(join_code)

    for row in board:
        for spot in row:
            if (get_num_player(join_code, spot["name"]) == 1):
                player1 = True
            elif (get_num_player(join_code, spot["name"]) == 2):
                player2 = True
            elif (get_num_player(join_code, spot["name"]) == 3):
                player3 = True
            elif (get_num_player(join_code, spot["name"]) == 4):
                player4 = True

    if (not player1):
        remove_player(join_code, 1)
    if (not player2):
        remove_player(join_code, 2)
    if (not player3):
        remove_player(join_code, 3)
    if (not player4):
        remove_player(join_code, 4)

    split_teams(join_code)
