"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    for row in board:
        for cell in row:
            if cell == 'X':
                countX += 1
            if cell == 'O':
                countO += 1

    if countX > countO:
        return 'O'
    
    if countO >= countO:
        return 'X'
    
    return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == None:
                possible_actions.append((x, y))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    new_board = copy.deepcopy(board)
    x,y = action
    new_board[x][y] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_combinations = [
        ((0,0), (0,1), (0,2)),
        ((1,0), (1,1), (1,2)),
        ((2,0), (2,1), (2,2)),
        ((0,0), (1,0), (2,0)),
        ((0,1), (1,1), (2,1)),
        ((0,2), (1,2), (2,2)),
        ((0,0), (1,1), (2,2)),
        ((0,2), (1,1), (2,0))
    ]

    for (x1,y1), (x2,y2), (x3,y3) in winning_combinations:
        if board[x1][y1] == board[x2][y2] == board[x3][y3] and board[x1][y1] != None:
            return board[x1][y1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_player = winner(board)
    if winner_player == 'X' or winner_player == 'O':
        return True
    
    for row in board:
        for cell in row:
            if cell == None:
                return False
    
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board) 

    if winner_player == 'X':
        return 1
    if winner_player == 'O':
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)
    best_action = None
    best_value = -99999 if current_player == 'X' else 99999

    for action in actions(board):
        new_board = result(board, action)

        if current_player == 'X':
            v = min_value(new_board)
            if v > best_value:
                best_value = v
                best_action = action
        else:
            v = max_value(new_board)
            if v < best_value:
                best_value = v
                best_action = action

    return best_action

    
def max_value(board):
    v = -999999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v,min_value(result(board,action)))
    return v

def min_value(board):
    v = 999999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
    return v
   