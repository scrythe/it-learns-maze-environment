import it_learns_mazes
import gymnasium as gym
import pygame
import time


# @profile
def episode():
    env.reset(seed=i, options={"size": 10})
    terminated = False
    truncated = False
    while not terminated and not truncated:
        action = 2
        obs, reward, terminated, truncated, info = env.step(action)


if __name__ == "__main__":
    env = gym.make("it-learns-mazes-v0")
    for i in range(5000):
        episode()
