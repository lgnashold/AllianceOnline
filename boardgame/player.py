from boardgame.db import get_db

import json

def add_player(join_code, nickname, money=300, team=None):
    """Adds a player to the game
    If games full, returns None, otherwise return player"""
    db = get_db()
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
            return player_obj
    return None

def remove_player(join_code, nickname):
    """Removes player from a game"""
    pass

def get_players(join_code):
    """returns a dictonary of all players in a game"""
    db = get_db()
    player_jsons = db.execute(
            "SELECT (player1, player2, player3, player4) FROM game WHERE join_code = (?)", (join_code,)).fetchone()
    players = {}
    for key, value in playerjsons.items():
        players[key] = json.loads(value)
    return players

