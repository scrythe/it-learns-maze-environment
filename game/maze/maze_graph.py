import numpy as np
from enum import Enum
import numpy.typing as npt


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def generate_maze_graph(size: int):
    total_cells_amount = size * size
    # size more than total cells amount because it does not only contain cells but also stop sequence and such
    # Size in most cases smaller but just incase (worst case scenario total_cells_amount*2-1)
    maze_graph = np.zeros((total_cells_amount * 3, 2), dtype=np.int32)
    visited_cells = np.zeros((size, size), dtype=np.int32)
    rand_visited_cell = np.random.randint(0, size, 2)
    visited_cells[rand_visited_cell[1], rand_visited_cell[0]] = 1
    current_cell_index = 0
    visited_cells_index = 1

    while visited_cells_index < total_cells_amount:
        current_sub_graph_cells = np.zeros((size, size), dtype=np.int32)
        current_cell = rand_unvisited_cell(
            visited_cells, visited_cells_index, total_cells_amount
        )
        current_cell_index, visited_cells_index = add_cell_to_lists(
            maze_graph,
            visited_cells,
            current_sub_graph_cells,
            current_cell,
            current_cell_index,
            visited_cells_index,
        )
        while True:
            rand_direction = get_random_direction(current_cell, size)
            new_cell = cell_goto_direction(current_cell, rand_direction)
            if check_cell_inside_list(current_sub_graph_cells, new_cell):
                current_cell_index, visited_cells_index = reverse_graph_to_cell(
                    maze_graph,
                    visited_cells,
                    current_sub_graph_cells,
                    new_cell,
                    current_cell_index,
                    visited_cells_index,
                )
                current_cell = new_cell
                continue
            if check_cell_inside_list(visited_cells, new_cell):
                maze_graph[current_cell_index] = new_cell
                current_cell_index += 1
                maze_graph[current_cell_index] = -1
                current_cell_index += 1
                break
            current_cell_index, visited_cells_index = add_cell_to_lists(
                maze_graph,
                visited_cells,
                current_sub_graph_cells,
                new_cell,
                current_cell_index,
                visited_cells_index,
            )
            current_cell = new_cell
    return maze_graph


def rand_unvisited_cell(
    visited_cells: npt.NDArray, visited_cells_index: int, total_cells_amount: int
):
    available_cells = total_cells_amount - visited_cells_index - 1
    available_cells_index = 0
    rand_cell_index = np.random.randint(0, available_cells + 1)
    for y_pos, row in enumerate(visited_cells):
        for x_pos, cell in enumerate(row):
            if cell == 1:
                continue
            if available_cells_index == rand_cell_index:
                return [x_pos, y_pos]
            available_cells_index += 1


def reverse_graph_to_cell(
    maze_graph: npt.NDArray,
    visited_cells: npt.NDArray,
    current_sub_graph_cells: npt.NDArray,
    target_cell: npt.NDArray,
    cell_index: int,
    visited_cells_index: int,
):
    cell_index -= 1
    visited_cells_index -= 1
    current_cell = maze_graph[cell_index]
    while not (target_cell == current_cell).all():
        visited_cells[current_cell[1], current_cell[0]] = 0
        current_sub_graph_cells[current_cell[1], current_cell[0]] = 0
        cell_index -= 1
        visited_cells_index -= 1
        current_cell = maze_graph[cell_index]
    cell_index += 1
    visited_cells_index += 1
    return cell_index, visited_cells_index


def add_cell_to_lists(
    maze_graph: npt.NDArray,
    visited_cells: npt.NDArray,
    current_sub_graph_cells: npt.NDArray,
    cell: npt.NDArray,
    cell_index: int,
    visited_cells_index: int,
):
    visited_cells[cell[1], cell[0]] = 1
    current_sub_graph_cells[cell[1], cell[0]] = 1
    maze_graph[cell_index] = cell
    cell_index += 1
    visited_cells_index += 1
    return cell_index, visited_cells_index


def get_random_direction(current_cell: npt.NDArray, size: int):
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
