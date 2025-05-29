from .maze_graph import reverse_graph_to_cell, rand_unvisited_cell
import numpy as np


def test_random_unvisited_cell():
    visited_cells = np.array([[1, 1, 0], [0, 1, 1], [0, 1, 1]], dtype=np.int32)
    visited_cells_index = 6
    total_cells_amount = 9
    for _ in range(20):
        rand_cell = rand_unvisited_cell(
            visited_cells,
            visited_cells_index,
            total_cells_amount,
            np.random.default_rng(),
        )
        # print(rand_cell)
        assert not visited_cells[rand_cell[1], rand_cell[0]].any()


def test_reverse_graph_to_cell():
    maze_graph = np.array(
        [
            [0, 0],
            [1, 0],
            [2, 0],
            [2, 1],
            [2, 2],
            [1, 2],
            [1, 1],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ],
        dtype=np.int32,
    )
    visited_cells = np.array([[1, 1, 1], [0, 1, 1], [0, 1, 1]], dtype=np.int32)
    current_sub_graph_cells = visited_cells.copy()
    new_cell = np.array([2, 1])
    current_cell_index = 7
    visited_cells_index = 7

    current_cell_index, visited_cells_index = reverse_graph_to_cell(
        maze_graph,
        visited_cells,
        current_sub_graph_cells,
        new_cell,
        current_cell_index,
        visited_cells_index,
    )

    expected_visited_cells = np.array([[1, 1, 1], [0, 0, 1], [0, 0, 0]], dtype=np.int32)
    expected_sub_graph_cells = expected_visited_cells.copy()
    assert (visited_cells == expected_visited_cells).all()
    assert (current_sub_graph_cells == expected_sub_graph_cells).all()
    assert current_cell_index == 4
    assert visited_cells_index == 4
