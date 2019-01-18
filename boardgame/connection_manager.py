from boardgame.db import get_db
import json


def addPlayer(join_code, playernum):
    # Adds a player to the list of connected players
    l = get_list(join_code)
    if playernum not in l:
        l.append(playernum)
        set_list(playernum, l)


def removePlayer(join_code, playernum):
    # Removes a player from the list of connected players
    l = get_list(join_code)
    if playernum in l:
        l.remove(playernum)
        set_list(join_code, l)


def numberOfPlayers(join_code):
    return len(get_list(join_code))


def get_list(join_code):
    db = get_db()
    db.execute("SELECT connections FROM game WHERE join_code = (%s)", (join_code,))
    result = db.fetchone()
    if result is None:
        return None
    if result["connections"] is None:
        return []
    return json.loads(result["connections"])


def set_list(join_code, newlist):
    db = get_db()
    jsonres = json.dumps(newlist)
    db.execute("UPDATE game SET connections = (%s) WHERE join_code = (%s)", (jsonres, join_code))
