use pyo3::prelude::*;

#[pymodule]
fn exacting(m: &Bound<'_, PyModule>) -> PyResult<()> {
    Ok(())
}
