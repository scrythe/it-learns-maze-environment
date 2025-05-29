import it_learns_mazes
import gymnasium as gym
import pygame
from line_profiler import profile
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
    start_time = time.time()
    for i in range(5000):
        episode()
    print("--- %s seconds ---" % (time.time() - start_time))
