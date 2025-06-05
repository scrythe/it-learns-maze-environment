use pyo3::prelude::*;
use rand::{rngs, SeedableRng};
mod longest_path_maze;
mod maze_graph;
mod maze_structure;
mod raycaster;

#[pyfunction]
fn generate_maze_structure(size: usize, np_seed: u128) -> (Vec<Vec<i32>>, [i32; 2]) {
    let mut seed = [0u8; 32];
    let np_seed = np_seed.to_be_bytes();
    seed[..16].copy_from_slice(&np_seed);
    let mut rng = rngs::StdRng::from_seed(seed);

    let maze_graph = maze_graph::generate_maze_graph(&mut rng, size);
    let mut maze_structure = maze_structure::convert_graph_to_structure(size, maze_graph);

    let [start, goal] = longest_path_maze::find_longest_path(&mut rng, &maze_structure);
    maze_structure[goal[1] as usize][goal[0] as usize] = maze_structure::GOAL;

    (maze_structure, start)
}

#[pymodule]
fn maze_env_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<raycaster::Raycaster>()?;
    // m.add_function(wrap_pyfunction!(maze_graph::generate_maze_graph, m)?)?;
    // m.add_function(wrap_pyfunction!(
    //     maze_structure::convert_graph_to_structure,
    //     m
    // )?)?;
    m.add_function(wrap_pyfunction!(generate_maze_structure, m)?)?;
    // m.add_function(wrap_pyfunction!(longest_path_maze::find_longest_path, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_maze_structure() {
        generate_maze_structure(5, 0);
    }
}
