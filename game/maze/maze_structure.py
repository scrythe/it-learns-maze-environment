import numpy as np
import numpy.typing as npt
from .constants import PATH
from .maze_graph import generate_maze_graph


def generate_maze_structure(size: int):
    maze_graph = generate_maze_graph(size)
    maze_structure = convert_graph_to_structure(maze_graph, size)
    return maze_structure


def convert_graph_to_structure(maze_graph: npt.NDArray, size: int):
    structure_size = size * 2 + 1
    maze_structure = np.zeros((structure_size, structure_size), dtype=np.int32)
    prev_cell_pos = maze_graph[0] * 2 + 1
    for cell in maze_graph:
        if (cell == -1).all():
            prev_cell_pos = cell
            continue
        cell_pos = cell * 2 + 1
        maze_structure[cell_pos[1], cell_pos[0]] = PATH
        if (prev_cell_pos == -1).all():
            prev_cell_pos = cell_pos
            continue
        between_cell_pos = (cell_pos - prev_cell_pos) // 2
        between_cell_pos = prev_cell_pos + between_cell_pos
        maze_structure[between_cell_pos[1], between_cell_pos[0]] = PATH
        prev_cell_pos = cell_pos
    return maze_structure
