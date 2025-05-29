from maze_env_rust import Raycaster
from .maze import generate_maze_structure
import math
import numpy as np


def test_raycaster():
    raycaster = Raycaster(40, 90, 3)
    maze_structure = generate_maze_structure(5, 0)
    raycaster.reset(maze_structure)
    raycaster.cast_multiple_rays(
        (40.5, 40.5),
        0,
    )
    raycaster.cast_multiple_rays(
        (40.5, 40.5),
        math.pi,
    )
    raycaster.cast_multiple_rays(
        (40.5, 40.5),
        1 / 2 * math.pi,
    )
    raycaster.cast_multiple_rays(
        (40.5, 40.5),
        3 / 2 * math.pi,
    )
