from boardgame.db import get_db
import json

def get_list(join_code):
    db = get_db()
    result = db.execute("SELECT players FROM lobby WHERE join_code = (?)", (join_code, )).fetchone()
    if result == None:
        return None
    if(result["players"] == None):
        return []
    return json.loads(result["players"])


def set_list(join_code, newlist):
    db = get_db()
    jsonres = json.dumps(newlist)
    db.execute("UPDATE lobby SET players = (?) WHERE join_code = (?)", (jsonres, join_code))
    db.commit()
