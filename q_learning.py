from collections import defaultdict

import gym
from board import COLUMNS, ROWS
# env = gym.make('4InARow/Sag-Env')

import numpy as np
import random
from IPython.display import clear_output
import fourinarow
import fourinarow.envs
import gym
from gym import envs
print(envs.registry)
enviroment = gym.make('FourInARow/Sag-Env').env
enviroment.reset()
enviroment.render()

print(f'{enviroment.observation_space=}')
print(f'{enviroment.action_space=}')

alpha = 0.1
gamma = 0.6
epsilon = 0.1
# q_table = np.zeros([COLUMNS*ROWS, enviroment.action_space.n])
# q_table = np.ones([COLUMNS*ROWS, enviroment.action_space.n])
# q_table = np.zeros([COLUMNS, ROWS, 7])
q_table = {}

# num_of_episodes = 100000
num_of_episodes = 10


def random_column(board):
    possible_columns = list(range(COLUMNS))
    while len(possible_columns) > 0:
        col = random.choice(possible_columns)
        if board[col][0] != 0:
            possible_columns.remove(col)
        else:
            return col

    raise Exception(f"couldn't find a column in board: {board}")


for episode in range(0, num_of_episodes):
    obs = enviroment.reset()
    state = obs['state']
    player = obs['p']
    board = obs['board']
    print(f"{state=}")

    # Initialize variables
    reward = 0
    terminated = False

    while not terminated:
        # Take learned path or explore new actions based on the epsilon
        if random.uniform(0, 1) < epsilon:
            # action = enviroment.action_space.sample()
            action = random_column(board=board)
        else:
            if state in q_table:
                if np.max(q_table[state]) == 0:
                    action = enviroment.action_space.sample()
                else:
                    action = np.argmax(q_table[state])
            else:
                q_table[state] = {1: 0, 2: 0}
                action = random_column(board=board)

        # Take action
        next_state, reward, terminated, info = enviroment.step(action)
        if terminated:
            print(f"game ended! reward = {reward} on state = {state}")

        # Recalculate
        try:
            q_value = q_table[state].get(player)
            # max_value = np.max(q_table[next_state])
            max_value = 0.5
            new_q_value = (1 - alpha) * q_value + alpha * (reward + gamma * max_value)

            # Update Q-table
            q_table[state][player] = new_q_value
            state = next_state['state']
            if state not in q_table:
                q_table[state] = {1: 0, 2: 0}
            board = next_state['board']
            player = next_state['p']
        except Exception as e:
            print(f"error - {e}")
            raise

    if (episode + 1) % 100 == 0:
        clear_output(wait=True)
        print("Episode: {}".format(episode + 1))
        enviroment.render()

print("**********************************")
print("Training is done!\n")
print(f"{q_table=}")
print("**********************************")