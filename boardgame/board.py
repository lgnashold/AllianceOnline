BOARD_WIDTH = 3
BOARD_HEIGHT = 3
DEFAULT_SQUARE = {"color":"ff0055"}

import json
from boardgame.db import get_db

def create_board(join_code):
    board = []
    for row in range(BOARD_WIDTH):
            board.append([])
            for col in range(BOARD_HEIGHT):
                board[row].append(DEFAULT_SQUARE)
    set_board(board, join_code)

def set_board(board, join_code):
    """Given a board array, saves it to sql database"""
    json_board = json.dumps(board) 
    db = get_db()
    db.execute(
            'UPDATE game SET board = (?) WHERE join_code = (?)', (json_board, join_code)
    );
    db.commit;
    
def get_board(join_code):
    json_board = db.execute(
            "SELECT board FROM game WHERE join_code = (?)", (join_code,)
    );
    board = json.loads(json_board)
    return board
