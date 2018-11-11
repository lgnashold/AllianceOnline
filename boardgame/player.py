from boardgame.db import get_db

from boardgame.players import get_players 
import json

def set_turn(join_code, player_num):
    """Set's the player whose turn it currently is"""
    db = get_db()
    db.execute(
            "UPDATE game SET turn = (?) WHERE join_code = (?)", (player_num, join_code)
    )
    db.commit()

def get_turn(join_code):
    """Get the number of the player whose turn it currently is"""
    db = get_db()
    turn = db.execute(
        "SELECT turn FROM game WHERE join_code = (?)", (join_code,)
    ).fetchone()["turn"]
    return turn

def increment_turn(join_code):
    """Sets turn to the next valid player"""
    players = get_players()
    turn = get_turn(join_code)
    turn = (turn % 4) + 1
    while(players["player" + str(turn)] == None):
        turn = (turn % 4) + 1
    set_turn(turn)
