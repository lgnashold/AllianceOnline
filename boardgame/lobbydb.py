from boardgame.db import get_db
import json

def get_list(join_code):
    db = get_db()
    db.execute("SELECT players FROM lobby WHERE join_code = (%s)", (join_code, ))
    result = db.fetchone()
    if result == None:
        return None
    if(result["players"] == None):
        return []
    return json.loads(result["players"])


def set_list(join_code, newlist):
    db = get_db()
    jsonres = json.dumps(newlist)
    db.execute("UPDATE lobby SET players = (%s) WHERE join_code = (%s)", (jsonres, join_code))

def remove_list(join_code):
    db = get_db()
    db.execute("DELETE FROM lobby WHERE join_code = (%s)", (join_code,))
