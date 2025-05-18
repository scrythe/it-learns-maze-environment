from gymnasium.envs.registration import register

register(
    id="it-learns-mazes-v0",
    entry_point="it_learns_mazes.environment:MazeEnv",
)
