import numpy as np
from enum import Enum
import numpy.typing as npt


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def generate_maze_structure(size: int):
    maze_graph = generate_maze_graph(size)


def generate_maze_graph(size: int):
    total_cells_amount = size * size
    # Total cellls amount times two because it does not only contain cells but also stop sequence
    # Size in most cases smaller but just incase (worst case scenario total_cells_amount*2-1)
    maze_graph = np.zeros((total_cells_amount * 2, 2), dtype=np.int32)
    visited_cells = np.zeros((size, size), dtype=np.int32)
    current_cell_index = 0
    visited_cells_index = 0

    while current_cell_index < total_cells_amount - 1:
        current_sub_graph_cells = np.zeros((size, size), dtype=np.int32)
        current_cell = np.random.randint(0, size, 2)
        current_cell_index, visited_cells_index = add_cell_to_lists(
            maze_graph,
            visited_cells,
            current_sub_graph_cells,
            current_cell,
            current_cell_index,
            visited_cells_index,
        )
        while True:
            if visited_cells_index >= total_cells_amount - 1:
                return maze_graph
            rand_direction = get_random_directions(current_cell, size)
            new_cell = cell_goto_direction(current_cell, rand_direction)
            if check_cell_inside_list(current_sub_graph_cells, new_cell):
                current_cell_index, visited_cells_index = reverse_graph_to_cell(
                    maze_graph,
                    visited_cells,
                    current_sub_graph_cells,
                    current_cell,
                    current_cell_index,
                    visited_cells_index,
                )
                continue
            current_cell_index, visited_cells_index = add_cell_to_lists(
                maze_graph,
                visited_cells,
                current_sub_graph_cells,
                new_cell,
                current_cell_index,
                visited_cells_index,
            )
            current_cell = new_cell
            if check_cell_inside_list(visited_cells, new_cell):
                maze_graph[current_cell_index] = [-1, -1]
                current_cell_index += 1
                break
    return maze_graph


def reverse_graph_to_cell(
    maze_graph: npt.NDArray,
    visited_cells: npt.NDArray,
    current_sub_graph_cells: npt.NDArray,
    target_cell: npt.NDArray,
    cell_index: int,
    visited_cells_index: int,
):
    current_cell = maze_graph[cell_index]
    while (target_cell != current_cell).all():
        visited_cells[current_cell[1]][current_cell[0]] = 0
        current_sub_graph_cells[current_cell[1]][current_cell[0]] = 1
        cell_index -= 1
        visited_cells_index -= 1
        current_cell = maze_graph[cell_index]
    return cell_index, visited_cells_index


def add_cell_to_lists(
    maze_graph: npt.NDArray,
    visited_cells: npt.NDArray,
    current_sub_graph_cells: npt.NDArray,
    cell: npt.NDArray,
    cell_index: int,
    visited_cells_index: int,
):
    visited_cells[cell[1]][cell[0]] = 1
    current_sub_graph_cells[cell[1]][cell[0]] = 1
    maze_graph[cell_index] = cell
    cell_index += 1
    visited_cells_index += 1
    return cell_index, visited_cells_index


def get_random_directions(current_cell: npt.NDArray, size: int):
    possible_directions: list[Direction] = []
    if current_cell[1] > 0:
        possible_directions.append(Direction.UP)
    if current_cell[0] < size - 1:
        possible_directions.append(Direction.RIGHT)
    if current_cell[1] < size - 1:
        possible_directions.append(Direction.DOWN)
    if current_cell[0] > 0:
        possible_directions.append(Direction.LEFT)

    rand_direction_index = np.random.randint(0, len(possible_directions))
    rand_direction = possible_directions[rand_direction_index]
    return rand_direction


def check_cell_inside_list(list: npt.NDArray, cell: npt.NDArray):
    return list[cell[1]][cell[0]] == 1


def cell_goto_direction(current_cell: npt.NDArray, direction: Direction):
    new_cell = current_cell.copy()
    if direction == Direction.UP:
        new_cell[1] -= 1
    if direction == Direction.RIGHT:
        new_cell[0] += 1
    if direction == Direction.DOWN:
        new_cell[1] += 1
    if direction == Direction.LEFT:
        new_cell[0] -= 1
    return new_cell


if __name__ == "__main__":
    generate_maze_graph(10)
