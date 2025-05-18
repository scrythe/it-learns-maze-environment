import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from .game import Game


class MazeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 1}

    def __init__(self, render_mode=None):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.game = Game()
        self.screen = None
        self.clock = None
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)

    def _get_obs(self):
        pass

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # initialise and reset
        obs = self._get_obs()
        return obs

    def render(self):
        pygame.event.pump()
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((320, 320))
        if self.clock is None:
            self.clock = pygame.Clock()
        self.game.draw(self.screen)
        self.clock.tick(self.metadata["render_fps"])

    def step(self, action):
        # perform action
        if self.render_mode == "human":
            self.render()

        obs = self._get_obs()
        return obs
