from boardgame.db import get_db
from boardgame.board import *
from boardgame.colors import *
from boardgame.emissions import emit_money
import json
from psycopg2 import sql


def add_player(join_code, nickname, money=300, team=None):
    """Adds a player to the game
    If games full, returns None, otherwise return player"""
    db = get_db()
    players = get_players(join_code)
    player_obj = {}

    player_obj["money"] = money
    player_obj["nickname"] = nickname

    # checks for dups
    for key, value in players.items():
        if value != None and value["nickname"] == nickname:
            return None

    # Checks for column to add player
    count = 0
    for key, value in players.items():
        count+=1
        if value == None:
            player_obj["team"] = "team" + str(count)
            db.execute(
                    sql.SQL("UPDATE game SET {} = (%s) WHERE join_code = (%s)").format(Identifier(key)), (json.dumps(player_obj), join_code)
                    )
            return count
    return None

def remove_player(join_code, player_num):
    print("REMOVING PLAYER " + str(player_num))
    """Removes player from a game"""
    update_player(join_code,player_num,None)

def get_players(join_code):
    """returns a dictonary of all players in a game"""
    db = get_db()
    db.execute("SELECT player1, player2, player3, player4 FROM game WHERE join_code = (%s)", (join_code,))
    player_jsons = dict(db.fetchone())
    players = {}
    for key, value in player_jsons.items():
        if value != None:
            players[key] = json.loads(value)
        else:
            players[key] = None
    return players

def get_player(join_code,player_num):
    players = get_players(join_code)
    return players["player" + str(player_num)]

def update_player_money(join_code,player_num,moneyChange):
    db = get_db()
    old_player = get_players(join_code)["player" + str(player_num)]
    if old_player == None:
        return None

    old_player["money"] += moneyChange

    update_player(join_code,player_num, old_player)
    emit_money(join_code,get_players(join_code))

def update_player_team(join_code,player_num,team_name):
    db = get_db()
    player = get_players(join_code)["player" + str(player_num)]
    if player == None:
        return None
    board = get_board(join_code)


    player["team"] = team_name

    update_player(join_code,player_num, player)

    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j]["name"] == player["nickname"]):
                board[i][j]["color"] = colors[player["team"]]
                print(board[i][j])
    set_board(join_code, board)

def num_players_on_team(join_code,team_name):
    players = get_players(join_code)
    count = 0;

    for key,value in players.items():
        if(value != None and team_name == value["team"]):
            count+=1

    return count

def get_num_players(join_code):
    players = get_players(join_code)
    count = 0;

    for key,value in players.items():
        if(value != None):
            count+=1

    return count

def get_num_player(join_code, nickname):
    players = get_players(join_code)

    count = 0;
    for key,value in players.items():
        count+=1
        if(value != None and value["nickname"] == nickname):
            return count

    return None

def update_player(join_code, player_num, player_obj):
    db = get_db()

    db.execute(
            SQL("UPDATE game SET {} = (%s) WHERE join_code = (%s)").format(Identifier("player" + str(player_num))), (json.dumps(player_obj), join_code)
            )
