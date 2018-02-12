from collections import Counter
from collections import deque
import random

import gym
from gym import error, spaces, utils
from gym.envs.classic_control import rendering
from gym.utils import seeding

class SnakeAction(object):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class SnakeCellState(object):
    EMPTY = 0
    WALL = 1
    DOT = 2

class SnakeReward(object):
    ALIVE = -0.1
    DOT = 5
    DEAD = -100
    WON = 100

class SnakeGame(object):
    def __init__(self, width, height, head):
        self.width = width
        self.height = height

        self.snake = deque()
        self.empty_cells = {(x, y) for x in range(width) for y in range(height)}
        self.dot = None

        self.prev_action = SnakeAction.UP

        self.add_to_head(head)
        self.generate_dot()

    def add_to_head(self, cell):
        self.snake.appendleft(cell)
        if cell in self.empty_cells:
            self.empty_cells.remove(cell)
        if self.dot == cell:
            self.dot = None

    def cell_state(self, cell):
        if cell in self.empty_cells:
            return SnakeCellState.EMPTY
        if cell == self.dot:
            return SnakeCellState.DOT
        return SnakeCellState.WALL

    def head(self):
        return self.snake[0]

    def remove_tail(self):
        tail = self.snake.pop()
        self.empty_cells.add(tail)

    def can_generate_dot(self):
        return len(self.empty_cells) > 0

    def generate_dot(self):
        self.dot = random.sample(self.empty_cells, 1)[0]
        self.empty_cells.remove(self.dot)

    def is_valid_action(self, action):
        if len(self.snake) == 1:
            return True

        horizontal_actions = [SnakeAction.LEFT, SnakeAction.RIGHT]
        vertical_actions = [SnakeAction.UP, SnakeAction.DOWN]

        if self.prev_action in horizontal_actions:
            return action in vertical_actions
        
        return action in horizontal_actions

    def next_head(self, action):
        head_x, head_y = self.head()
        if action == SnakeAction.LEFT:
            return (head_x - 1, head_y)
        if action == SnakeAction.RIGHT:
            return (head_x + 1, head_y)
        if action == SnakeAction.UP:
            return (head_x, head_y + 1)
        return (head_x, head_y - 1)

    def step(self, action):
        if not self.is_valid_action(action):
            action = self.prev_action
        self.prev_action = action

        next_head = self.next_head(action)
        next_head_state = self.cell_state(next_head)

        if next_head_state == SnakeCellState.WALL:
            return SnakeReward.DEAD

        self.add_to_head(next_head)
        
        if next_head_state == SnakeCellState.DOT:
            if self.can_generate_dot():
                self.generate_dot()
                return SnakeReward.DOT                
            return SnakeReward.WON
        
        self.remove_tail()
        return SnakeReward.ALIVE


class SnakeExtraHardEnv(gym.Env):
    metadata= {'render.modes': ['human']}

    # TODO: define observation_space
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = None

        self.width = 40
        self.height = 40
        self.start = (10, 10)

        self.game = SnakeGame(self.width, self.height, self.start)
        self.viewer = None

    # TODO: define observation, info
    def step(self, action):
        reward = self.game.step(action)

        done = reward in [SnakeReward.DEAD, SnakeReward.WON]
        observation = None
        info = None

        return observation, reward, done, info

    # TODO: define observation
    def reset(self):
        self.game = SnakeGame(self.width, self.height, self.start)
        observation = None
        return observation

    def render(self, mode='human', close=False):
        width = height = 600
        width_scaling_factor = width / self.width
        height_scaling_factor = height / self.height

        if self.viewer is None:
            self.viewer = rendering.Viewer(width, height)

        for x, y in self.game.snake:
            l, r, t, b = x*width_scaling_factor, (x+1)*width_scaling_factor, y*height_scaling_factor, (y+1)*height_scaling_factor
            square = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            square.set_color(0, 0, 0)
            self.viewer.add_onetime(square)

        if self.game.dot:
            x, y = self.game.dot
            l, r, t, b = x*width_scaling_factor, (x+1)*width_scaling_factor, y*height_scaling_factor, (y+1)*height_scaling_factor
            square = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            square.set_color(1, 0, 0)
            self.viewer.add_onetime(square)

        return self.viewer.render(return_rgb_array=mode=='rgb_array')

    def close(self):
        pass

    def seed(self):
        pass
