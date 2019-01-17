from boardgame.db import get_db
from boardgame.player import get_players

import json

def set_turn(join_code, player_num):
    db = get_db()
    db.execute("UPDATE game SET turn = (%s) WHERE join_code = (%s)", (player_num, join_code))

def get_turn(join_code):
    db = get_db()
    db.execute("SELECT turn FROM game WHERE join_code = (%s)", (join_code,))
    turn = db.fetchone()["turn"]
    return turn

def increment_turn(join_code):
    turn = get_turn(join_code)
    turn = (turn % 4) + 1
    players = get_players(join_code)
    while(players["player" + str(turn)] == None):
        turn = (turn % 4) + 1
    set_turn(join_code, turn)
    return turn
