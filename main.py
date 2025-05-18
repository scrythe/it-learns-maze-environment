import it_learns_mazes
import gymnasium as gym

if __name__ == "__main__":
    env = gym.make("it-learns-mazes-v0")
    env.reset()
    terminated = False
    truncated = False
    while not terminated or not truncated:
        obs, reward, terminated, truncated, info = env.step(0)
        terminated = True
