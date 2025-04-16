mod converter;
use crate::converter::extract_strategy;
use pyo3::prelude::*;
use pyo3::types::PyDict;

pyo3::import_exception!(kanalizer._error, IncompleteConversionError);
pyo3::import_exception!(kanalizer._error, InvalidCharsError);
pyo3::import_exception!(kanalizer._error, EmptyInputError);

#[pyfunction]
#[pyo3(signature = (word, /, *, max_length = 32, strict = true, error_on_incomplete = true, strategy = "greedy", **kwargs))]
fn convert(
    word: &str,
    max_length: usize,
    strict: bool,
    error_on_incomplete: bool,
    strategy: &str,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<String> {
    let strategy = extract_strategy(strategy, kwargs)?;
    let result = kanalizer::convert(word)
        .with_max_length(max_length.try_into().map_err(|_| {
            pyo3::exceptions::PyValueError::new_err("max_length must be a positive integer")
        })?)
        .with_strategy(&strategy)
        .with_strict(strict)
        .with_error_on_incomplete(error_on_incomplete)
        .perform();

    match result {
        Ok(dst) => Ok(dst),
        Err(err @ kanalizer::Error::EmptyInput) => Err(EmptyInputError::new_err(err.to_string())),
        Err(ref err @ kanalizer::Error::InvalidChars { ref chars }) => Err(
            InvalidCharsError::new_err((err.to_string(), chars.to_vec())),
        ),
        Err(
            ref err @ kanalizer::Error::IncompleteConversion {
                ref incomplete_output,
            },
        ) => Err(IncompleteConversionError::new_err((
            err.to_string(),
            incomplete_output.to_owned(),
        ))),
    }
}

#[pymodule(name = "_rust")]
fn init_kanalizer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("INPUT_CHARS", &*kanalizer::INPUT_CHARS)?;
    m.add("OUTPUT_CHARS", &*kanalizer::OUTPUT_CHARS)?;
    m.add_function(wrap_pyfunction!(convert, m)?)?;

    Ok(())
}
