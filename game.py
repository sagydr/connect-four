import random

from board import COLUMNS, ROWS, Board, Players, Token
from enum import Enum


class FourInLine:
    def __init__(self):
        self.board = Board()
        self.current_player = Players.P1
        self.move_counter = 0

    def reset(self):
        self.board = Board()
        self.current_player = Players.P1
        self.move_counter = 0

    def play(self, column):
        player = self.current_player
        token = Token.get(player=self.current_player)
        self.board.play(token=token, column=column)
        self.current_player = Players.P1 if player == Players.P2 else Players.P2
        self.move_counter += 1
        print(f"player {player} played move {self.move_counter}")
        return token, player

    def get_state(self):
        state = ''
        for col in range(COLUMNS):
            for row in range(ROWS):
                state += str(self.board.board[col][row])

        return state

    def is_game_over(self, token):
        board = self.board.board

        # Horizontal checker
        for col in range(3, COLUMNS):
            for row in range(0, ROWS):
                if board[col][row] == board[col-1][row] == board[col-2][row] == board[col-3][row] == token.value:
                    return True

        # Vertical checker
        for col in range(0, COLUMNS):
            for row in range(3, ROWS):
                if board[col][row] == board[col][row-1] == board[col][row-2] == board[col][row-3] == token.value:
                    return True

        # Diagonal checker
        for col in range(0, 4):
            for row in range(0, 3):
                if (board[col][row] == board[col + 1][row + 1] == board[col + 2][row + 2] == board[col + 3][row + 3] == token.value or
                        board[col + 3][row] == board[col + 2][row + 1] == board[col + 1][row + 2] == board[col][row + 3] == token.value):
                    return True

        return False


if __name__ == '__main__':
    game = FourInLine()
    print(game.get_state())
    while True:
        game.board.render()
        col = int(input(f"input column for {game.current_player}"))
        if col in {1, 2, 3, 4, 5, 6, 7}:
            col = col-1  # zero based
            token, player_played = game.play(col)
            if game.is_game_over(token=token):
                print(f"game finished! winner = {player_played}")
                break
        else:
            print("please enter column between 1-7")
