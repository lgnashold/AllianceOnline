from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from boardgame.db import get_db

from boardgame.board import create_board
from boardgame.player import add_player, get_players
from boardgame.turn import get_turn
from boardgame.lobbydb import get_list, set_list
bp = Blueprint("matchmaking", __name__)

@bp.route("/", methods = ('GET','POST'))
def index():
    if request.method == "POST":
        nickname = request.form['nickname']
        join_code = request.form['join_code']

        db = get_db()

        players = get_list(join_code) 
       
        #TODO HERE: Check if game is not already started
        game = db.execute("SELECT * FROM game WHERE join_code = (?)", (join_code,)).fetchone()
        if game != None:
            print("ERROR: Game has already started")
            return render_template("index.html")

        if players is None:
            #create new game
            db.execute(
                'INSERT INTO lobby (join_code) VALUES (?)', (join_code,)
            )
            db.commit()
            players = get_list(join_code)
    
        if len(players) >= 4:
            print("ERROR: Game " + join_code + " IS FULL")
            return render_template("index.html")
        if players.count(nickname) != 0:
            print("ERROR: Game " + join_code + "  already has name "+nickname)
            return render_template("index.html")
        
        players.append(nickname)
        set_list(join_code, players)

        # Updates session variables
        session["join_code"] = join_code
        session["nickname"] = nickname

        return redirect(url_for('lobby.enter_lobby'))

    # Run if request is GET
    return render_template("index.html")
