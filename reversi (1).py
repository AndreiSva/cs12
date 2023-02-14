# Reversi AI

import random
import time
import copy

board = [[" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", "○", "●", " ", " ", " "],
         [" ", " ", " ", "●", "○", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "]]

# 8 directions to check for flipping other player's pieces
directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                (-1, 0), (-1, -1), (0, -1), (1, -1)]

def display(board):
    """Prints out a formatted version of board."""
    print("-----------------")
    for row in board:
        row_string = "|"
        for space in row:
            row_string += space + "|" 
        print(row_string)
        print("-----------------")

def on_board(x, y):
    """Returns True if the position at (x, y) is on the board."""
    return 0 <= x <= 7 and 0 <= y <= 7

def next_player(player):
    """Returns the piece of the next player to play)"""
    if player == "●":
        return "○"
    else:
        return "●"

def play(board, piece, x, y):
    """If playing at (x, y) is legal, plays piece there and returns True.
       Otherwise leaves board unchanged and returns False."""
    if board[y][x] != " ":
        return False
    pieces_to_flip = []
    for i, j in directions:
        x_now = x+i
        y_now = y+j
        pieces_to_add = []
        # Continue in direction while you encounter other player's pieces
        while on_board(x_now, y_now) and board[y_now][x_now] not in [piece, " "]:
            pieces_to_add.append((x_now, y_now))
            x_now += i
            y_now += j
        # If next piece is your own, flip all pieces in between
        if on_board(x_now, y_now) and board[y_now][x_now] == piece:
            pieces_to_flip += pieces_to_add
    # Move is legal if any pieces are flipped
    if pieces_to_flip != []:
        board[y][x] = piece
        for i, j in pieces_to_flip:
            board[j][i] = piece
        return True
    else:
        return False


# -----------------------
# Your functions to write
# -----------------------

def evaluate(board):
    """Returns an evaluation of the board.
       A score of zero indicates a neutral position.
       A positive score indicates that black is winning.
       A negative score indicates that white is winning."""
    b = 0
    w = 0
    for row in board:
        b += row.count("●")
        w += row.count("○")
    return b - w

def max_moves(board, player):
    """Returns a list of tuples (x, y) representing the moves that have
       the highest evaluation score for the given player."""
    possiblemoves = []
    maxmoves = []

    enemy = None
    if player == "●":
        enemy = "○"
    else:
        enemy = "●"

    # we need to get every possible move for our turn
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == enemy:
                for x, y in directions:
                    if on_board(j+x, i+y) and board[i+y][j+x] == " ":
                        bboard = copy.deepcopy(board)
                        if play(bboard, player, j+x, i+y) == True:
                            possiblemoves.append((j+x, i+y))
                    
    return maxmoves

def minimax_moves(board, player):
    """Returns a list of tuples (x, y) representing the moves that give
       the opposing player the worst possible evaluation score for the
       best of their next moves."""

# -----------------------
# -----------------------

current_player = "●"
while True:
    if current_player == "●":
        moves = max_moves(board, current_player)
    else:
        moves = minimax_moves(board, current_player)
    if moves == []:
        break
    else:
        # Play a random move from the best moves
        x, y = random.choice(moves)
        play(board, current_player, x, y)
        current_player = next_player(current_player)
        time.sleep(0.5)
        
    



                
    
    
