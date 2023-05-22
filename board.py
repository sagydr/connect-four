import numpy as np
from enum import Enum

import pygame

COLUMNS = 7
ROWS = 6
DISPLAY_WINDOW_SIZE = 512
DISPLAY_SQUARE_SIZE = 100


class Players(Enum):
    P1 = 1
    P2 = 2


class Token(Enum):
    RED = 1
    BLUE = 2

    @staticmethod
    def get(player: Players):
        return Token.RED if player == Players.P1 else Token.BLUE


class Board:
    def __init__(self):
        # self.board = np.zeros([enviroment.observation_space.n, enviroment.action_space.n])
        self.board = []
        for _ in range(COLUMNS):
            self.board.append([0] * ROWS)
        self._window = None
        self._clock = None

    def place_token(self, token: Token, column: int):
        for row in reversed(range(ROWS)):
            if self.board[column][row] == 0:
                self.board[column][row] = token.value
                break

    def play(self, token: Token, column: int):
        # assert legal move
        self.place_token(token=token, column=column)

    # def render(self):
    #     for i in reversed(range(ROWS)):
    #         print(f"{i}) ", end=' ')
    #         for j in range(COLUMNS):
    #             print(self.board[j][i], end=" ")
    #             print(' | ', end=' ')
    #         print("")

    def _init_render(self, human_render=True):
        if self._window is None and human_render:
            pygame.init()
            pygame.display.init()
            self._window = pygame.display.set_mode((DISPLAY_SQUARE_SIZE * COLUMNS, DISPLAY_SQUARE_SIZE * ROWS))
        if self._clock is None and human_render:
            self._clock = pygame.time.Clock()

    def render(self, human_render=True, highlight_squares=None):
        self._init_render()

        # 0,0 is TOP LEFT
        canvas = pygame.Surface((DISPLAY_SQUARE_SIZE * COLUMNS, DISPLAY_SQUARE_SIZE * ROWS))
        canvas.fill((255, 255, 255))
        pix_square_size = DISPLAY_SQUARE_SIZE  # The size of a single grid square in pixels

        shift = DISPLAY_SQUARE_SIZE / 2
        for c in range(COLUMNS):
            col = self.board[c]
            for r in range(ROWS):
                if col[r] != 0:
                    # print(f"placing ({(c, r)}) circle in {(c * DISPLAY_SQUARE_SIZE + shift, r * DISPLAY_SQUARE_SIZE + shift)}")

                    pygame.draw.circle(
                        canvas,
                        (0, 0, 255) if col[r] == Token.BLUE.value else (255, 0, 0),
                        ((c * DISPLAY_SQUARE_SIZE) + shift, (r * DISPLAY_SQUARE_SIZE) + shift),
                        DISPLAY_SQUARE_SIZE/5,  # radius
                    )
                    if highlight_squares and (c, r) in highlight_squares:
                        pygame.draw.rect(
                            canvas,
                            (10,255,10),
                            pygame.Rect((c * DISPLAY_SQUARE_SIZE),
                                        (r * DISPLAY_SQUARE_SIZE),
                                        DISPLAY_SQUARE_SIZE,
                                        DISPLAY_SQUARE_SIZE),
                            20,  # width
                        )

        # Finally, add some gridlines
        for x in range(COLUMNS + 1):
            # print(f"drawing ({(0, pix_square_size * x)}) -> ({(DISPLAY_SQUARE_SIZE * COLUMNS, pix_square_size * x)})")
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (DISPLAY_SQUARE_SIZE * COLUMNS, pix_square_size * x),
                width=3,
            )
            # print(f"drawing {(pix_square_size * x, 0)} -> ({(pix_square_size * x, DISPLAY_SQUARE_SIZE * ROWS)})")
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, DISPLAY_SQUARE_SIZE * ROWS),
                width=3,
            )

        if human_render:
            # The following line copies our drawings from `canvas` to the visible window
            self._window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self._clock.tick(0)
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        return canvas


if __name__ == '__main__':
    board = Board()
    board.play(token=Token.RED, column=2)
    board.play(token=Token.BLUE, column=4)
    board.play(token=Token.RED, column=4)
    # board.play(token=Token.BLUE, column=5)
    # board.place_token(Token.RED, 0, 2)
    # board.place_token(Token.BLUE, 2, 1)
    board.render()
    print(f"done")
