# from .environment import MazeEnv
from gymnasium.utils.env_checker import check_env
import gymnasium as gym


def test_custom_env():
    env = gym.make("it-learns-mazes-v0")
    check_env(env.unwrapped)


def test_maze_seed_reset():
    env = gym.make("it-learns-mazes-v0")
    env.reset(seed=5, options={"size": 3})
    maze_structure = env.unwrapped.game.maze_structure
    env.reset(seed=5, options={"size": 3})
    second_maze_structure = env.unwrapped.game.maze_structure
    assert (maze_structure == second_maze_structure).all()


def test_environment_seed_reset():
    env = gym.make("it-learns-mazes-v0")
    obs1, _ = env.reset(seed=5, options={"size": 3})
    obs2, _ = env.reset(seed=5, options={"size": 3})
    assert (obs1 == obs2).all()
