use pyo3::prelude::*;
use rand::{rngs, Rng, SeedableRng};

const VISITED: bool = true;
const UNVISITED: bool = false;

#[pyfunction]
pub fn generate_maze_graph(size: usize, np_seed: u128) -> Vec<[i32; 2]> {
    let mut seed = [0u8; 32];
    let np_seed = np_seed.to_be_bytes();
    seed[..16].copy_from_slice(&np_seed);
    let mut rng = rngs::StdRng::from_seed(seed);

    let total_cells_amount = size * size;
    let mut maze_graph: Vec<[i32; 2]> = vec![[0; 2]; total_cells_amount * 3];
    let mut visited_cells = vec![vec![false; size]; size];
    let total_cells_amount = size * size;
    let mut current_cell_index = 0;
    let mut visited_cells_index = 1;

    let rand_first_visited_cell: [usize; 2] = [rng.random_range(..size), rng.random_range(..size)];
    visited_cells[rand_first_visited_cell[1]][rand_first_visited_cell[0]] = VISITED;

    while visited_cells_index < total_cells_amount {
        let mut current_sub_graph_cells: Vec<Vec<bool>> = vec![vec![false; size]; size];
        let mut current_cell = create_rand_unvisited_cell(
            &mut rng,
            total_cells_amount,
            &visited_cells,
            visited_cells_index,
        );
        add_cell_to_lists(
            current_cell,
            &mut current_cell_index,
            &mut visited_cells_index,
            &mut visited_cells,
            &mut current_sub_graph_cells,
            &mut maze_graph,
        );

        loop {
            let rand_direction = get_random_direction(&mut rng, size, current_cell);
            let new_cell = create_cell_goto_direction(current_cell, rand_direction);
            if check_cell_inside(new_cell, &current_sub_graph_cells) {
                reverse_graph_to_cell(
                    new_cell,
                    &mut current_cell_index,
                    &mut visited_cells_index,
                    &mut visited_cells,
                    &mut current_sub_graph_cells,
                    &mut maze_graph,
                );
                current_cell = new_cell;
                continue;
            }
            if check_cell_inside(new_cell, &visited_cells) {
                maze_graph[current_cell_index] = new_cell;
                maze_graph[current_cell_index + 1] = [-1, -1];
                current_cell_index += 2;
                break;
            }
            add_cell_to_lists(
                new_cell,
                &mut current_cell_index,
                &mut visited_cells_index,
                &mut visited_cells,
                &mut current_sub_graph_cells,
                &mut maze_graph,
            );
            current_cell = new_cell
        }
    }
    maze_graph
}

fn create_rand_unvisited_cell(
    rng: &mut rngs::StdRng,
    total_cells_amount: usize,
    visited_cells: &Vec<Vec<bool>>,
    visited_cells_index: usize,
) -> [i32; 2] {
    let available_cells_amount = total_cells_amount - visited_cells_index - 1;
    let rand_available_cell_index = rng.random_range(..available_cells_amount + 1);
    let mut current_available_cell_index = 0;
    for (y_pos, row) in visited_cells.iter().enumerate() {
        for (x_pos, cell) in row.iter().enumerate() {
            if *cell == VISITED {
                continue;
            }
            if current_available_cell_index == rand_available_cell_index {
                return [x_pos as i32, y_pos as i32];
            }
            current_available_cell_index += 1;
        }
    }
    panic!("No available cells")
}

fn add_cell_to_lists(
    cell: [i32; 2],
    cell_index: &mut usize,
    visited_cells_index: &mut usize,
    visited_cells: &mut Vec<Vec<bool>>,
    current_sub_graph_cells: &mut Vec<Vec<bool>>,
    maze_graph: &mut Vec<[i32; 2]>,
) {
    visited_cells[cell[1] as usize][cell[0] as usize] = VISITED;
    current_sub_graph_cells[cell[1] as usize][cell[0] as usize] = VISITED;
    maze_graph[*cell_index] = cell;
    *cell_index += 1;
    *visited_cells_index += 1;
}

#[derive(Clone)]
enum Direction {
    UP,
    RIGHT,
    DOWN,
    LEFT,
}

fn get_random_direction(rng: &mut rngs::StdRng, size: usize, current_cell: [i32; 2]) -> Direction {
    let mut possible_directions = vec![];

    if current_cell[1] > 0 {
        possible_directions.push(Direction::UP);
    }
    if current_cell[0] < size as i32 - 1 {
        possible_directions.push(Direction::RIGHT);
    }
    if current_cell[1] < size as i32 - 1 {
        possible_directions.push(Direction::DOWN);
    }
    if current_cell[0] > 0 {
        possible_directions.push(Direction::LEFT);
    }

    let rand_direction_index = rng.random_range(..possible_directions.len());
    let rand_direction = possible_directions[rand_direction_index].clone();
    rand_direction
}

fn create_cell_goto_direction(mut current_cell: [i32; 2], direction: Direction) -> [i32; 2] {
    match direction {
        Direction::UP => current_cell[1] -= 1,
        Direction::RIGHT => current_cell[0] += 1,
        Direction::DOWN => current_cell[1] += 1,
        Direction::LEFT => current_cell[0] -= 1,
    }
    current_cell
}

fn check_cell_inside(cell: [i32; 2], list: &Vec<Vec<bool>>) -> bool {
    list[cell[1] as usize][cell[0] as usize]
}

fn reverse_graph_to_cell(
    target_cell: [i32; 2],
    current_cell_index: &mut usize,
    visited_cells_index: &mut usize,
    visited_cells: &mut Vec<Vec<bool>>,
    current_sub_graph_cells: &mut Vec<Vec<bool>>,
    maze_graph: &mut Vec<[i32; 2]>,
) {
    *current_cell_index -= 1;
    *visited_cells_index -= 1;
    let mut current_cell = maze_graph[*current_cell_index];
    while target_cell != current_cell {
        visited_cells[current_cell[1] as usize][current_cell[0] as usize] = UNVISITED;
        current_sub_graph_cells[current_cell[1] as usize][current_cell[0] as usize] = UNVISITED;
        *current_cell_index -= 1;
        *visited_cells_index -= 1;
        current_cell = maze_graph[*current_cell_index]
    }
    *current_cell_index += 1;
    *visited_cells_index += 1;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_random_unvisited_cell() {
        let visited_cells = vec![
            vec![VISITED, VISITED, UNVISITED],
            vec![UNVISITED, VISITED, VISITED],
            vec![UNVISITED, VISITED, VISITED],
        ];
        let visited_cells_index = 6;
        let total_cells_amount = 9;
        let mut rng = rngs::StdRng::seed_from_u64(0);
        for _ in 0..20 {
            let rand_cell = create_rand_unvisited_cell(
                &mut rng,
                total_cells_amount,
                &visited_cells,
                visited_cells_index,
            );
            let is_visited = visited_cells[rand_cell[1] as usize][rand_cell[0] as usize];
            print!("{:?}", rand_cell);
            assert!(!is_visited)
        }
    }

    #[test]
    fn test_generate_maze_graph() {
        generate_maze_graph(5, 0);
    }
}
