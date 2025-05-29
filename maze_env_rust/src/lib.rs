use pyo3::prelude::*;
mod maze_graph;
mod raycaster;

#[pymodule]
fn maze_env_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<raycaster::Raycaster>()?;
    m.add_function(wrap_pyfunction!(maze_graph::generate_maze_graph, m)?)?;
    Ok(())
}
