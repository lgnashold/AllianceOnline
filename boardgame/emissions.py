from . import socketio
from boardgame.board import get_json_board

from flask_socketio import emit

def emit_message(msg, join_code, channel = "/game"):
    """Emits a message to the whole server"""
    socketio.emit('message', {"data":msg, "room":join_code}, broadcast = True, namespace=channel)

def emit_board(join_code):
    socketio.emit('update_board', {"board":get_json_board(join_code),"room":join_code}, broadcast = True, namespace="/game")

def emit_money(join_code, players, channel="/game"):
    socketio.emit('update_money', {"data":players, "room":join_code}, broadcast = True, namespace=channel)

def emit_error(msg, join_code):
    """Emits an error to just one player"""
    socketio.emit('error', {"data":msg}, namespace='/game')
    
def emit_turn(join_code, nickname):
    print("Emit turn")
    socketio.emit('update_turn', {"data":nickname, "room":join_code}, broadcast = True, namespace="/game")

def emit_end_game(join_code, nickname):
    socketio.emit("end_game", {"data":nickname, "room":join_code}, broadcast = True, namespace = "/game")

def emit_teams(join_code, teamcolors, players) :
        socketio.emit('update_teams', {"players": players, "colors":teamcolors, 'room':join_code}, broadcast=True, namespace = "/game")
