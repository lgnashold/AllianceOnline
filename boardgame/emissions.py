from boardgame.board import get_json_board

from flask_socketio import emit

def emit_message(msg, join_code):
    emit('message', {"data":msg, "room":join_code}, broadcast = True)

def emit_board(join_code):
    emit('update_board', {"board":get_json_board(join_code),"room":join_code}, broadcast = True)

def emit_money(join_code,players):
    emit('update_money', {"data":players, "room":join_code, broadcast = True)
