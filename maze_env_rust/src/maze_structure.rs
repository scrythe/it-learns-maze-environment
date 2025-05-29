use pyo3::prelude::*;

const PATH: i32 = 1;

#[pyfunction]
pub fn convert_graph_to_structure(size: usize, maze_graph: Vec<[i32; 2]>) -> Vec<Vec<i32>> {
    let structure_size = size * 2 + 1;
    let mut maze_structure = vec![vec![0; structure_size]; structure_size];
    let mut prev_cell_pos = maze_graph[0];
    prev_cell_pos[0] = prev_cell_pos[0] * 2 + 1;
    prev_cell_pos[1] = prev_cell_pos[1] * 2 + 1;
    for cell in maze_graph.iter() {
        if cell[0] == -1 {
            prev_cell_pos = cell.clone();
            continue;
        }
        let cell_pos = [cell[0] * 2 + 1, cell[1] * 2 + 1];
        maze_structure[cell_pos[1] as usize][cell_pos[0] as usize] = PATH;
        if prev_cell_pos[0] == -1 {
            prev_cell_pos = cell_pos;
            continue;
        }
        let between_cell_pos_x = prev_cell_pos[0] + (cell_pos[0] - prev_cell_pos[0]) / 2;
        let between_cell_pos_y = prev_cell_pos[1] + (cell_pos[1] - prev_cell_pos[1]) / 2;
        maze_structure[between_cell_pos_y as usize][between_cell_pos_x as usize] = PATH;
        prev_cell_pos = cell_pos;
    }
    maze_structure
}
