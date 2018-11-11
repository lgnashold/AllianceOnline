from boardgame.db import get_db

from boardgame.players import get_players 
import json

def set_turn(join_code, player_num):
    """Set's the player whose turn it currently is"""
    db = get_db()
<<<<<<< HEAD
    players = get_players(join_code)
    player_obj = {}

    player_obj["money"] = money
    player_obj["nickname"] = nickname

    count = 0
    for key, value in players.items():
        count+=1
        if value == None:
            player_obj["team"] = "team" + str(count)
            db.execute(
                    "UPDATE game SET %s = (?) WHERE join_code = (?)" % key, (json.dumps(player_obj), join_code)
                    )
            db.commit()
            session["player_num"] = count
            return player_obj
    return None

def remove_player(join_code, nickname):
    """Removes player from a game"""
    pass

def get_players(join_code):
    """returns a dictonary of all players in a game"""
=======
    db.execute(
            "UPDATE game SET turn = (?) WHERE join_code = (?)", (player_num, join_code)
    )
    db.commit()

def get_turn(join_code):
    """Get the number of the player whose turn it currently is"""
>>>>>>> 40a1c89b76709e108ae2a9372522010e2f93ad00
    db = get_db()
    turn = db.execute(
        "SELECT turn FROM game WHERE join_code = (?)", (join_code,)
    ).fetchone()["turn"]
    return turn

<<<<<<< HEAD
def get_player(join_code,nickname):
    players = get_players(join_code)
    for key, value in players:
        if(value['nickname'] == nickname):
            return value
    return none

def update_player_money(join_code,nickname,moneyChange):
    db = get_db()
    old_player = get_player(join_code,nickname)
    if old_playe == None:
        return None
    player_obj = {}

    player_obj["money"] = old_player["money"] + moneyChange
    player_obj["nickname"] = old_player["nickname"]

    db.execute(
            "UPDATE game SET %s = (?) WHERE join_code = (?)" % key, (json.dumps(player_obj), join_code)
            )
    db.commit()
=======
def increment_turn(join_code):
    """Sets turn to the next valid player"""
    players = get_players()
    turn = get_turn(join_code)
    turn = (turn % 4) + 1
    while(players["player" + str(turn)] == None):
        turn = (turn % 4) + 1
    set_turn(turn)
>>>>>>> 40a1c89b76709e108ae2a9372522010e2f93ad00
