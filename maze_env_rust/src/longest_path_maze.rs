use rand::{rngs, Rng};

use crate::maze_structure;

fn depth_first_search(
    rng: &mut rngs::StdRng,
    maze_structure: &Vec<Vec<i32>>,
    start: &[i32; 2],
) -> [i32; 2] {
    let mut current_cell = start.clone();
    let mut longest_cell = current_cell;
    let maze_len = maze_structure.len();
    let mut stack: Vec<[i32; 2]> = Vec::with_capacity(maze_len);
    let mut visited_cells = vec![vec![false; maze_len]; maze_len];
    visited_cells[current_cell[1] as usize][current_cell[0] as usize] = true;
    stack.push(current_cell);
    let mut longest_length = stack.len();
    loop {
        print_visited_cells(&visited_cells, longest_cell);
        if let Some(rand_cell) = get_random_cell(rng, maze_structure, &visited_cells, current_cell)
        {
            current_cell = rand_cell;
            visited_cells[current_cell[1] as usize][current_cell[0] as usize] = true;
            stack.push(current_cell);
            if longest_length <= stack.len() {
                longest_length = stack.len();
                longest_cell = current_cell;
            }
            continue;
        }
        if let Some(prev_cell) = stack.pop() {
            current_cell = prev_cell;
            continue;
        }
        break longest_cell;
    }
}

enum Directions {
    UP,
    RIGHT,
    DOWN,
    LEFT,
}

fn print_visited_cells(visited_cells: &Vec<Vec<bool>>, longest_cell: [i32; 2]) {
    print!("\x1B[2J\x1B[1;1H");
    for (row_i, row) in visited_cells.iter().enumerate() {
        for (cell_i, cell) in row.iter().enumerate() {
            if cell_i == longest_cell[0] as usize && row_i == longest_cell[1] as usize {
                print!("2");
                continue;
            }
            let cell = *cell as i32;
            print!("{}", cell);
        }
        println!();
    }
}

fn get_random_cell(
    rng: &mut rngs::StdRng,
    maze_structure: &Vec<Vec<i32>>,
    visited_cells: &Vec<Vec<bool>>,
    current_cell: [i32; 2],
) -> Option<[i32; 2]> {
    let mut possible_moves: Vec<Directions> = Vec::with_capacity(4);
    let above_cell_y = current_cell[1] - 1;
    let right_cell_x = current_cell[0] + 1;
    let down_cell_y = current_cell[1] + 1;
    let left_cell_x = current_cell[0] - 1;
    let current_cell_x = current_cell[0] as usize;
    let current_cell_y = current_cell[1] as usize;

    if maze_structure[above_cell_y as usize][current_cell_x] == maze_structure::PATH
        && !visited_cells[above_cell_y as usize][current_cell_x]
    {
        possible_moves.push(Directions::UP);
    }
    if maze_structure[current_cell_y][right_cell_x as usize] == maze_structure::PATH
        && !visited_cells[current_cell_y][right_cell_x as usize]
    {
        possible_moves.push(Directions::RIGHT);
    }
    if maze_structure[down_cell_y as usize][current_cell_x] == maze_structure::PATH
        && !visited_cells[down_cell_y as usize][current_cell_x]
    {
        possible_moves.push(Directions::DOWN);
    }
    if maze_structure[current_cell_y][left_cell_x as usize] == maze_structure::PATH
        && !visited_cells[current_cell_y][left_cell_x as usize]
    {
        possible_moves.push(Directions::LEFT);
    }

    if possible_moves.len() <= 0 {
        return None;
    }

    let rand_direction_index = rng.random_range(..possible_moves.len());
    let rand_direction = &possible_moves[rand_direction_index];

    match rand_direction {
        Directions::UP => Some([current_cell_x as i32, above_cell_y]),
        Directions::RIGHT => Some([right_cell_x, current_cell_y as i32]),
        Directions::DOWN => Some([current_cell_x as i32, down_cell_y]),
        Directions::LEFT => Some([left_cell_x, current_cell_y as i32]),
    }
}

pub fn find_longest_path(rng: &mut rngs::StdRng, maze_structure: &Vec<Vec<i32>>) -> [[i32; 2]; 2] {
    let start = [1, 1];
    let end_b = depth_first_search(rng, maze_structure, &start);
    let end_a = depth_first_search(rng, maze_structure, &end_b);
    [end_a, end_b]
}
