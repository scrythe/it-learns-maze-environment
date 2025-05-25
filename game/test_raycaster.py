from .raycaster import Raycaster
from .maze import generate_maze_structure
import math


def test_raycaster():
    raycaster = Raycaster(40, 90, 1)
    maze_structure = generate_maze_structure(5)
    raycaster.reset(maze_structure)
    raycaster.cast_single_ray(
        (20.5, 20.5),
        0,
        0,
    )
    raycaster.cast_single_ray(
        (20.5, 20.5),
        math.pi,
        math.pi,
    )
    raycaster.cast_single_ray(
        (20.5, 20.5),
        1 / 2 * math.pi,
        1 / 2 * math.pi,
    )
    raycaster.cast_single_ray(
        (20.5, 20.5),
        3 / 2 * math.pi,
        3 / 2 * math.pi,
    )
