import random
import numpy as np

from game import winning_move
from board import COLUMNS, ROWS, Board, Token


def random_board_generator():
    # board = np.zeros([COLUMNS, ROWS])
    board = Board()
    for c in range(COLUMNS):
        for r in range(ROWS):
            rand = random.random()
            if 0.75 < rand < 1:
                board.place_token(Token.RED, c, r)
            elif 0.5 < rand < 0.75:
                board.place_token(Token.BLUE, c, r)
    return board


def test_random():
    board = random_board_generator()
    print(board.board)
    board.render()
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board.board[c][r] != 0.0:
                if winning_move(board, board.board[c][r], c, r):
                    print(f"{c},{r} ({board.board[c][r]}) is a winning move!")
