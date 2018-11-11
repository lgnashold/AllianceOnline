BOARD_WIDTH = 20
BOARD_HEIGHT = 20

DEFAULT_SQUARE = {"color":"#B9B7A7","name":None}

import json

from boardgame.db import get_db

from boardgame.colors import colors
from boardgame.player import remove_player, get_num_player

def create_board(join_code):
    print("called create board")
    board = []
    for row in range(BOARD_WIDTH):
            board.append([])
            for col in range(BOARD_HEIGHT):
                board[row].append(DEFAULT_SQUARE)
    set_board(join_code, board)
    return board

def set_board(join_code, board):
    """Given a board array, saves it to sql database"""
    json_board = json.dumps(board)
    db = get_db()
    db.execute(
            'UPDATE game SET game_data = (?) WHERE join_code = (?)', (json_board, join_code)
    );
    db.commit();
    return json_board

def get_board(join_code):
    return json.loads(get_json_board(join_code))

def get_json_board(join_code):
    db = get_db()
    json_board = (db.execute(
            "SELECT game_data FROM game WHERE join_code = (?)", (join_code,)
    ).fetchone())["game_data"]
    return json_board

def set_square(join_code, i, j, player, CheckAdjacency=False, CheckSameColor=False):
    board = get_board(join_code)
    new_color = colors[player["team"]]
    old_color = board[i][j]["color"]
    if (CheckSameColor and new_color == old_color):
        return "Your team already controls this square"
    if(CheckAdjacency and check_connected(join_code, i, j, new_color) < 1):
        return "Your team doesn't control enough adjacent squares"
    board[i][j] = {"color":new_color, "name": player["nickname"]}
    set_board(join_code, board)

def check_win(join_code):
    board = get_board(join_code)

    for row in range(board.length):
        for col in range(board[row].length):
            if (board[row][col] != board[0][0]):
                return False
    return True

def remove_no_territory(join_code):
    board = get_board(join_code)

    player1 = False
    player2 = False
    player3 = False
    player4 = False

    for row in range(len(board)):
        for col in range(len(board[row])):
            if (get_num_player(join_code,board[row][col]["nickname"]) == 1):
                player1 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 2):
                player2 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 3):
                player3 = True
            elif (get_num_player(join_code,board[row][col]["nickname"]) == 4):
                player4 = True

    if(not player1 and players.player1 != None):
        remove_player(1)
    if(not player2 and players.player2 != None):
        remove_player(2)
    if(not player3 and players.player3 != None):
        remove_player(3)
    if(not player4 and players.player4 != None):
        remove_player(4)

def check_connected(join_code, i, j, color):
    board = get_board(join_code)
    visited = [[False for i in row] for row in board]
    res = 0
    if(board[i][j]["color"] == color):
        res += 1
    res += check_connected_helper(board, i + 1, j, color, visited)
    res += check_connected_helper(board, i -1, j, color, visited)
    res += check_connected_helper(board, i, j+1, color, visited)
    res += check_connected_helper(board, i, j-1, color, visited)
    return res

def check_connected_helper(board, i, j, color, visited):
    if i < 0 or i >= len(visited) or j < 0 or j >= len(visited[0]):
        return 0
    if (visited[i][j] == True):
        return 0
    visited[i][j] = True
    if (board[i][j]["color"] != color):
        return 0
    res = 1
    res += check_connected_helper(board, i + 1, j, color, visited)
    res += check_connected_helper(board, i -1, j, color, visited)
    res += check_connected_helper(board, i, j+1, color, visited)
    res += check_connected_helper(board, i, j-1, color, visited)
    return res
