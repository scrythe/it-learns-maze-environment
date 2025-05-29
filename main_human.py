import it_learns_mazes
import gymnasium as gym
import pygame
from pyinstrument import Profiler


if __name__ == "__main__":
    env = gym.make("it-learns-mazes-v0", render_mode="human")
    for i in range(5):
        env.reset(seed=i)
        terminated = False
        truncated = False
        while not terminated and not truncated:
            pygame.init()
            pygame.display.init()
            keys = pygame.key.get_pressed()
            action = 3
            if keys[pygame.K_a]:
                action = 0
            elif keys[pygame.K_d]:
                action = 1
            elif keys[pygame.K_w]:
                action = 2
            obs, reward, terminated, truncated, info = env.step(action)
