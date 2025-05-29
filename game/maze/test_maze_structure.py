from .maze_structure import (
    convert_graph_to_structure,
)
from .maze_graph import generate_maze_graph
import numpy as np


def test_generate_maze_structure():
    for _ in range(20):
        size = 4
        maze_graph = generate_maze_graph(size, np.random.default_rng())
        maze_structure = convert_graph_to_structure(maze_graph, size)
        for y in range(size):
            for x in range(size):
                assert maze_structure[y * 2 + 1, x * 2 + 1] == 1


def test_convert_maze_structure():
    maze_graph = np.array(
        [
            [0, 0],
            [1, 0],
            [-1, -1],
            [0, 1],
            [0, 0],
            [-1, -1],
            [1, 1],
            [1, 0],
        ]
    )
    maze_structure = convert_graph_to_structure(maze_graph, 2)
    # print(maze_structure)
    expected_structure = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    assert (maze_structure == expected_structure).all()
