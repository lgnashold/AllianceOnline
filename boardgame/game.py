COST_EMPTY_SQUARE = 100
def COST_FILLED_SQUARE(numconnected):
    return 75+numconnected * 25
COST_TEAM_SWITCH=100
PROFIT_PER_SQUARE=50
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

import math

import json

@bp.route("/game")
def run_game():
    """"Serves game page"""
    return render_template("game.html", join_code = session["join_code"], nickname = session["nickname"], team_colors = colors);

@socketio.on('connect', namespace="/game")
def connect():
    join_code = session["join_code"]
    print(join_code)
    emit_board(join_code)
    emit_money(join_code, get_players(join_code))
    emit_teams(join_code, colors, get_players(join_code))
    emit_message("%s joined the game!" % session["nickname"], join_code)
    player = get_player(join_code, get_turn(join_code))
    print(player)
    emit_turn(join_code, player["nickname"])

@socketio.on('end_turn', namespace ="/game")
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
        for row in board:
            for space in row:
                if space["name"] == player["nickname"]:
                    spaces += 1
        money = spaces * PROFIT_PER_SQUARE
        update_player_money(join_code, turn, money)
        emit_turn(join_code, player["nickname"])


@socketio.on('disconnect', namespace="/game")
def disconnect():
    join_code = session["join_code"]
    print("DISCONNECT")
    emit_message("%s left the game..." % session["nickname"], join_code)
    make_squares_empty(join_code,session["player_num"])
    remove_player(join_code,session["player_num"])
    split_teams(join_code)

def split_teams(join_code):
    #checks if two final players are on same team, if so fixes that
    team = "none"
    count = 0
    if (get_num_players(join_code) == 2):
        count+=1
        players = get_players(join_code)
        for key,value in players.items():
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
                if(board[row][col]["name"] == get_player(join_code,player_num)["nickname"]):
                    board[row][col] = get_default_square()
    set_board(join_code, board)


@socketio.on('make_move', namespace ="/game")
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
            cost = COST_EMPTY_SQUARE
        else:
            # Otherwise does 30 times num of connected squares
            cost = COST_FILLED_SQUARE(cost)
        if player["money"] >= cost :
            errormsg = set_square(join_code, i, j, player, player_initiated=True)
            if(errormsg == None):
                update_player_money(join_code, player_num, -1 * cost)
                remove_no_territory(join_code)
                emit_board(join_code)
                gameover = test_end_game()
                if gameover:
                    emit_end_game(join_code, nickname)
                    return
                if (player["money"] - cost  < 100):
                    end_turn()

            else:
                emit_error(errormsg, join_code)
                print(errormsg)
        else:
            emit_error("Not enough money", join_code)
@socketio.on('change_team', namespace = "/game")
def change_team(data):
    join_code = session["join_code"]
    nickname = session["nickname"]
    player_num = session["player_num"]
    team = data["team"]
    player = get_player(join_code, player_num)

    if player_num == get_turn(join_code):
        if num_players_on_team(join_code, team) >=  math.ceil(get_num_players(join_code)/2 ):
            emit_error("There are already do many people on that team", join_code)
        elif player["money"] < COST_TEAM_SWITCH:
            emit_error("You do not have enough money to switch teams!", join_code)
        else:
            update_player_money(join_code, player_num, -1 * COST_TEAM_SWITCH)
            update_player_team(join_code, player_num, team)
            emit_message("Player {0} changed to {1}!".format(nickname, team), join_code)
            emit_board(join_code)
            emit_teams(join_code, colors, get_players(join_code))

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

    split_teams(join_code)


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
    if(len(names) <= 1):
        return True
    return False

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
    remove_player(session["join_code"],session["player_num"])
