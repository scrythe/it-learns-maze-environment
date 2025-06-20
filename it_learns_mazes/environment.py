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
        self.observation_space = spaces.Box(
            low=0, high=self.game.cell_width * 20, shape=(6,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(2)
        self.current_episode = 0

        if render_mode == "human":
            pygame.init()
            pygame.display.init()

    def reset(self, seed=None, options={"size": 5}):
        super().reset(seed=seed)
        if not options:
            options = {"size": 5}
        self.game.reset(options["size"], self.np_random_seed)
        info = {}
        return self._get_obs(), info

    def render(self):
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.game.maze_renderer.reset(self.game.maze_structure)
            self.game.rect = self.game.maze_renderer.image.get_rect()
            self.game.rect.width *= 2
            self.screen = pygame.display.set_mode(
                (self.game.rect.width, self.game.rect.height)
            )
            self.clock = pygame.Clock()

        pygame.event.pump()
        self.game.draw(self.screen)
        self.clock.tick(self.metadata["render_fps"])

    def _get_obs(self):
        return np.array(self.game.rays, dtype=np.float32)

    def step(self, action):
        terminated = False
        reward = 0
        truncated = False
        info = {}
        new_path = self.game.step(action)

        if self.game.collision:
            terminated = True
            reward -= 5
        if self.game.life_time <= 0:
            terminated = True
            reward -= 5

        if new_path:
            reward += 5

        obs = self._get_obs()

        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, truncated, info
