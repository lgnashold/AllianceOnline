from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from boardgame.db import get_db

from boardgame.board import create_board
from boardgame.player import add_player, get_players

bp = Blueprint("matchmaking", __name__)

@bp.route("/", methods = ('GET','POST'))
def index():
    if request.method == "POST":
        nickname = request.form['nickname']
        join_code = request.form['join_code']

        db = get_db()

        game_result = db.execute('SELECT player1, player2,join_code FROM game WHERE join_code = ?', (join_code,)).fetchone()

        if game_result is None:
            #create new game
            db.execute(
                'INSERT INTO game (join_code) VALUES (?)', (join_code,)
            )
            db.commit()
            # Creates a board, updates it in sql
            create_board(join_code)


        res = add_player(join_code, nickname)
        if(res == None):
            print("Game FULL")
            return render_template("index.html")

        session["player_num"] = res
        # Updates session variables
        session["join_code"] = join_code
        session["nickname"] = nickname

        return redirect(url_for('game.run_game'))

    # Run if request is GET
    return render_template("index.html")
