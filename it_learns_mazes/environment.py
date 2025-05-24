import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from game import Game


class MazeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode=None):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.game = Game()
        self.screen = None
        self.clock = None
        self.observation_space = spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)

    def _get_obs(self):
        return [0, 0, 0, 0, 0, 0]

    def reset(self, seed=None, options={"size": 5}):
        super().reset(seed=seed)
        np.random.seed(seed)
        if not options:
            options = {"size": 5}
        self.game.reset(options["size"])
        info = {}
        # initialise and reset
        obs = self._get_obs(), info
        return obs

    def render(self):
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (self.game.rect.width, self.game.rect.height)
            )
        if self.clock is None:
            self.clock = pygame.Clock()
        pygame.event.pump()
        self.game.draw(self.screen)
        self.clock.tick(self.metadata["render_fps"])

    def step(self, action):
        terminated = self.game.step(action)
        reward = 0
        truncated = False
        info = {}

        if self.render_mode == "human":
            self.render()

        obs = self._get_obs(), reward, terminated, truncated, info
        return obs
