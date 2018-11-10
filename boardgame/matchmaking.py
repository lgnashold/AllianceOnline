from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from boardgame.db import get_db

from boardgame.board import create_board

bp = Blueprint("matchmaking", __name__)

@bp.route("/", methods = ('GET','POST'))
def index():
    if request.method == "POST":
        nickname = request.form['nickname']
        join_code = request.form['join_code']

        db = get_db()

        game_result = db.execute('SELECT name1,name2,join_code FROM game WHERE join_code = ?', (join_code,)).fetchone()

        if game_result is None:
            #create new game
            db.execute(
                'INSERT INTO game (join_code,name1) VALUES (?,?)',(join_code,nickname)
            )
            db.commit()

            # Creates a board, updates it in sql
            create_board(join_code)

            # Updates session variables
            session["join_code"] = join_code
            session["nickname"] = nickname

            return redirect(url_for('game.run_game'))

        else:
            #join exsisting game
            if game_result["name2"] != None:
                print("SORRY PAL. GAME IS FULL");

            else:
                # Edits game row in server
                db.execute(
                    'UPDATE game SET name2 = (?) WHERE join_code = (?)',(nickname,join_code)
                )
                db.commit()

                session["join_code"] = game_result["join_code"]
                session["nickname"] = nickname
                return redirect(url_for('game.run_game'))

    # Run if request is GET
    return render_template("index.html")
