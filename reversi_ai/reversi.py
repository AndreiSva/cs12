# Reversi AI
# By Andrei Sova

import random
import time
import copy
from itertools import repeat

board = [[" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", "○", "●", " ", " ", " "],
         [" ", " ", " ", "●", "○", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " ", " "]]

testboard = [[" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "●", " ", " ", " ", " ", " "],
            [" ", " ", "●", "●", "●", " ", " ", " "],
            [" ", " ", " ", "○", "○", " ", " ", " "],
            [" ", " ", " ", "○", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "]]

# 8 directions to check for flipping other player's pieces
directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                (-1, 0), (-1, -1), (0, -1), (1, -1)]

black = "●"
white = "○"

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
    b, w = 0, 0
    for row in board:
        b += row.count("●")
        w += row.count("○")
    return b - w

def get_enemy(player):
    return white if player == black else black

def winning(player, score):
    return (player == black and score > 0) or (player == white and score < 0)

# this function is useful because it reduces code duplication between the max_moves and minmax_moves
def get_moves(board, player):
    """Returns a list of tuples that has all possible moves for a player,
       as well as a list of their evaluations"""
    possiblemoves = []
    possiblescores = []
    tried= []

    # this is needed for the useless optimization
    enemy = get_enemy(player)
    
    # we need to get every possible move for our turn
    # this loop is optimized to only search through fresh tiles adjacent to enemy tiles
    # the optimization doesn't matter that much since the board is only 7x7
    # but in theory it should be possible to run this on much bigger boards
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == enemy:
                # we check the adjacent tiles
                for x, y in directions:
                    # only try the adjacent coordinates if we haven't tried them before
                    if (j+x, i+y) not in tried:
                        # check if we're inside the board and that the tile is not filled
                        if on_board(j+x, i+y) and board[i+y][j+x] == " ":
                            bboard = copy.deepcopy(board)
                            # do the actual check
                            if play(bboard, player, j+x, i+y) == True:
                                possiblemoves.append(((j+x, i+y)))
                                possiblescores.append(evaluate(bboard))
                            tried.append((j+x, i+y))
                            
    return (possiblemoves, possiblescores)
    
def max_moves(board, player):
    """Returns a list of tuples (x, y) representing the moves that have
       the highest evaluation score for the given player."""
    moves, scores = get_moves(board, player)

    # we can't do any moves :(
    if len(moves) == 0:
        return []

    # what we're looking for
    target = max(scores) if player == black else min(scores)

    # we need only the coordinates that have our target value
    return list(filter(lambda x : scores[moves.index(x)] == target, moves))

def minimax_moves(board, player):
    """Returns a list of tuples (x, y) representing the moves that give
       the opposing player the worst possible evaluation score for the
       best of their next moves."""

    enemy = get_enemy(player)

    # this is the function we will use to find what we are looking for
    # (worst score for them)
    target_func = min if enemy == black else max
    
    # the moves that we can make
    moves = get_moves(board, player)[0] # we don't need the scores

    # the scores that the enemy will have after our move
    scores = []
    for move in moves:
        bboard = copy.deepcopy(board)

        # play our move
        play(bboard, player, move[0], move[1])

        # the enemy's best moves
        enemy_moves = max_moves(bboard, enemy)

        if len(enemy_moves) > 0:
            enemy_move = enemy_moves[0]
            
            # play the enemy's best move
            play(bboard, get_enemy(player), enemy_move[0], enemy_move[1])
            scores.append(evaluate(bboard))
        else:
            scores.append(0)

    # return all the moves that we can make that will yield the lowest score for our enemy in the next move
    score_indexes = filter(lambda x : scores[x] == target_func(scores), range(len(moves)))
    return list(map(lambda x : moves[x], score_indexes))

def minimax_smart(board, player, n = 4):
    """A recursive version of the minimax algorithm that looks
       up to n moves into the future. it is a bit slow"""

    # this function is incomplete
    
    enemy = get_enemy(player)
    target_func = max if enemy == black else min
    moves = minimax_moves(board, player)
    print(moves)
    if n < 1:
        if len(moves) > 0:
            bboard = copy.deepcopy(board)
            play(bboard, player, moves[0][0], moves[0][1])
            return (moves[0], evaluate(bboard)) # something
        else:
            return

    tree = []
    for move in moves:
        bboard = copy.deepcopy(board)
        play(bboard, player, move[0], move[1])

        enemy_moves = max_moves(bboard, enemy)

        if len(enemy_moves) > 0:
            enemy_move = enemy_moves[0]
            play(bboard, enemy, enemy_move[0], enemy_move[1])

        tree.append([(move, evaluate(bboard)), minimax_smart(bboard, player, n - 1)])

    moves_good = []
    return [target_func(filter(lambda x : type(x) == tuple, tree[0]), key = lambda x : x[1])[0]]

def algo_test(algo1, algo2, n = 50):
    """Runs a game between algo1 and algo2 n times and prints the win / loss ration for algo1"""
    wins = 0
    for i in range(n):
        current_board = copy.deepcopy(board)
        current_player = black
        while True:
            if current_player == black:
                moves = algo1(current_board, black)
            else:
                moves = algo2(current_board, white)
            if moves == []:
                if evaluate(current_board) > 0:
                    wins += 1
                break
            else:
                x, y = random.choice(moves)
                play(current_board, current_player, x, y)
                current_player = next_player(current_player)
    if wins != n:
        print(wins / (n - wins), str(wins / n * 100) + "% win rate")
    else:
        print(wins, "100% win rate")

# -----------------------
# -----------------------
def main():
    current_player = "●"
    while True:
        display(board)
        if current_player == "●":
            # moves = max_moves(board, current_player)
            moves = minimax_moves(board, current_player)
        else:
            moves = minimax_smart(board, current_player)
        if moves == []:
            display(board)
            score = evaluate(board)
            if score > 0:
                print("black wins")
            else:
                print("white wins")
            break
        else:
            # Play a random move from the best moves
            print(moves, current_player)
            x, y = random.choice(moves)
            play(board, current_player, x, y)
            current_player = next_player(current_player)
            time.sleep(0.5)
        
    

def test(): 
    board1 = [[" ", " ", " ", " ", " ", " ", " ", " "],
          ["○", " ", " ", " ", " ", " ", " ", " "],
          ["●", " ", " ", " ", " ", " ", " ", " "],
          ["●", " ", " ", "●", " ", " ", " ", " "],
          ["●", " ", "○", " ", " ", " ", " ", " "],
          ["●", "○", " ", " ", " ", " ", " ", " "],
          [" ", " ", " ", " ", " ", " ", " ", " "],
          [" ", "●", "●", "●", "●", "●", "●", "○"]]
    #print(minimax_moves(testboard, black))
    print(minimax_moves(board1, white))
    # main()

if __name__ == "__main__":
    test()
