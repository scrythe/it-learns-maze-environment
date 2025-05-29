use pyo3::prelude::*;
mod maze_graph;
mod maze_structure;
mod raycaster;

#[pyfunction]
fn generate_maze_structure(size: usize, seed: u128) -> Vec<Vec<i32>> {
    let maze_graph = maze_graph::generate_maze_graph(size, seed);
    let maze_structure = maze_structure::convert_graph_to_structure(size, maze_graph);
    maze_structure
}

#[pymodule]
fn maze_env_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<raycaster::Raycaster>()?;
    m.add_function(wrap_pyfunction!(maze_graph::generate_maze_graph, m)?)?;
    m.add_function(wrap_pyfunction!(
        maze_structure::convert_graph_to_structure,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(generate_maze_structure, m)?)?;
    Ok(())
}
