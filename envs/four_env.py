import random

import gym
from gym import spaces
import pygame
import numpy as np
from board import Board, COLUMNS, ROWS
from game import FourInLine


class ConnectFourEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode="human", size=5):
        self.columns = 7
        self.rows = 6
        self.window_size = 512  # The size of the PyGame window
        self.game = FourInLine()

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        # self.observation_space = spaces.Dict(
        #     {
        #         "board": spaces.Box(low=0, high=2, shape=(7,6,), dtype=int),
        #     }
        # )
        self.observation_space = spaces.Box(low=0, high=2, shape=(COLUMNS, ROWS, ), dtype=int)

        # We have 7 actions, one for each column
        self.action_space = spaces.Discrete(7)

        self._action_to_column = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
        }

        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _get_obs(self):
        # return {"board": self.game.board.board}
        # return self.game.board.board.copy()
        return {'state': self.game.get_state(),
                'p': self.game.current_player.value,
                'board': self.game.board.board}

    def _get_info(self):
        return {"state": self.game.get_state()}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # self.game.board = Board()
        self.game.reset()

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        # return observation, info
        return observation

    def render(self):
        # if self.render_mode == "rgb_array":
        #     return self._render_frame()
        return self.game.board.render()

    def _render_frame(self):
        # return self.board.render()
        return self.game.board.render()

    def random_column(self):
        possible_columns = list(range(COLUMNS))
        while len(possible_columns):
            col = random.choice(possible_columns)
            if self.game.board.board[col][ROWS-1] != 0:
                print(f"column {col} is full")
                possible_columns.remove(col)
            else:
                return col

    def step(self, action):
        column = action
        # We use `np.clip` to make sure we don't leave the grid

        token, player_played = self.game.play(column)
        terminated = self.game.is_game_over(token=token)
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        observation['p'] = player_played.value
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, info

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

