import numpy as np
from enum import Enum
import numpy.typing as npt


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def generate_maze_structure(size: int):
    maze_graph = _generate_maze_graph(size)


def _generate_maze_graph(size: int):
    visited_cells = np.zeros((size, size), dtype=np.int32)
    visited_cells_i = 0
    total_amount_cells = size * size - 1
    maze_graph = np.array([])
    stack = np.zeros((total_amount_cells - visited_cells_i, 2), dtype=np.int32)
    while visited_cells_i < total_amount_cells:
        current_cell = np.random.randint(0, size, 2)
        stack[visited_cells_i] = current_cell
        _make_cell_visited(visited_cells, current_cell)
        visited_cells_i += 1
        while True:
            if visited_cells_i < total_amount_cells:
                stack.resize((visited_cells_i - 1, 2))
                stack
            possible_directions = _get_possible_directions(current_cell, size)
            rand_direction_index = np.random.randint(0, len(possible_directions))
            direction = possible_directions[rand_direction_index]
            new_cell = cell_goto_direction(current_cell, direction)
            if _check_cell_visited(visited_cells, new_cell):
                break
            stack[visited_cells_i] = new_cell
            _make_cell_visited(visited_cells, current_cell)
            current_cell = new_cell
            visited_cells_i += 1
    stack.resize((visited_cells_i - 1, 2))
    print(maze_graph)


def _get_possible_directions(current_cell: npt.NDArray, size: int):
    possiblle_directions: list[Direction] = []
    if current_cell[1] > 0:
        possiblle_directions.append(Direction.UP)
    if current_cell[0] < size - 1:
        possiblle_directions.append(Direction.RIGHT)
    if current_cell[1] < size - 1:
        possiblle_directions.append(Direction.DOWN)
    if current_cell[0] > 0:
        possiblle_directions.append(Direction.LEFT)
    return possiblle_directions


def _make_cell_visited(visited_cells: npt.NDArray, cell: npt.NDArray):
    visited_cells[cell[1]][cell[0]] = 1


def _check_cell_visited(visited_cells: npt.NDArray, cell: npt.NDArray):
    return visited_cells[cell[1]][cell[0]] == 1


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

    def test_make_cell_visited():
        visited_cells = np.zeros((4, 4), dtype=np.int32)
        cell = (1, 2)
        _make_cell_visited(visited_cells, cell)
        correct_visited_cells = np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
            ]
        )
        if (visited_cells == correct_visited_cells).all():
            print("Test successful")
            return
        print("Test failed")

    def test_get_possible_directions():
        current_cell = (0, 0)
        possible_directiohns = _get_possible_directions(current_cell, 5)
        if (
            Direction.UP in possible_directiohns
            or Direction.LEFT in possible_directiohns
        ):
            print("Test failed")
            return
        current_cell = (4, 4)
        possible_directiohns = _get_possible_directions(current_cell, 5)
        if (
            Direction.RIGHT in possible_directiohns
            or Direction.DOWN in possible_directiohns
        ):
            print("Test failed")
            return
        print("Test successful")

    # test_make_cell_visited()
    # test_get_possible_directions()
    _generate_maze_graph(10)
