BOARD_WIDTH = 6
BOARD_HEIGHT = 6
# Revenue per square based on each square it's connected to
# For example, if you have one square, and it's connected to three
# squares of the same color, then that square generates $9
REVENUE_CONST = 5
BASE_REVENUE = 50
COST_EMPTY_SQUARE = 100
def COST_FILLED_SQUARE(numconnected):
    return 75+numconnected * 25

DEFAULT_SQUARE = {"color":"#B9B7A7","name":None}

import json
from flask import session
from boardgame.db import get_db

from boardgame.colors import colors

def create_board(join_code):
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
    db.execute('UPDATE game SET game_data = (%s) WHERE join_code = (%s)', (json_board, join_code))
    return json_board

def get_board(join_code):
    return json.loads(get_json_board(join_code))

def get_json_board(join_code):
    db = get_db()
    db.execute("SELECT game_data FROM game WHERE join_code = (%s)", (join_code,))
    json_board = (db.fetchone())["game_data"]
    return json_board

def set_square(join_code, i, j, player, player_initiated = False):
    board = get_board(join_code)
    new_color = colors[player["team"]]
    old_color = board[i][j]["color"]
    if (player_initiated and new_color == old_color):
        return "Your team already controls this square"
    if( player_initiated and check_connected(join_code, i, j, new_color) < 1):
        return "Square is not touching your color"
    board[i][j] = {"color":new_color, "name": player["nickname"]}
    set_board(join_code, board)

def get_default_square():
    return DEFAULT_SQUARE

def check_win(join_code):
    board = get_board(join_code)

    for row in range(board.length):
        for col in range(board[row].length):
            if (board[row][col] != board[0][0]):
                return False
    return True

def check_connected(join_code, i, j, color=None):
    board = get_board(join_code)
    if color == None:
        color = board[i][j]["color"]
    if color == DEFAULT_SQUARE["color"]:
        return -1
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

def get_revenue(join_code, nickname):
    #Naive implementation but working set is small
    board = get_board(join_code)
    tot = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]["name"] == nickname:
                tot += check_connected(join_code, row, col) * REVENUE_CONST + BASE_REVENUE
    return tot


def get_cost_of_square(i,j):
    cost = check_connected(session["join_code"], i, j, None)
    if cost == -1:
        cost = COST_EMPTY_SQUARE
    else:
        # Otherwise does 30 times num of connected squares
        cost = COST_FILLED_SQUARE(cost)
    return cost

def get_min_cost():
    board = get_board(session["join_code"])
    cost_list = []
    for row in range(len(board)):
        for col in range(len(board[row])):
                cost_list.append(get_cost_of_square(row, col))
    return min(cost_list)
