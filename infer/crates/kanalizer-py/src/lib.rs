mod converter;
use converter::{ErrorMode, extract_max_length, extract_strategy};
use pyo3::prelude::*;
use pyo3::types::PyDict;

pyo3::import_exception!(kanalizer._error, IncompleteConversionError);
pyo3::import_exception!(kanalizer._error, InvalidCharsError);
pyo3::import_exception!(kanalizer._error, EmptyInputError);
pyo3::import_exception!(kanalizer._error, IncompleteConversionWarning);
pyo3::import_exception!(kanalizer._error, InvalidCharsWarning);
pyo3::import_exception!(kanalizer._error, EmptyInputWarning);

#[pyfunction]
#[pyo3(signature = (word, /, *, max_length = kanalizer::MaxLength::Auto, on_invalid_input = ErrorMode::Error, on_incomplete = ErrorMode::Warning, strategy = "greedy", **kwargs))]
fn convert(
    py: Python,
    word: &str,
    #[pyo3(from_py_with = extract_max_length)] max_length: kanalizer::MaxLength,
    on_invalid_input: ErrorMode,
    on_incomplete: ErrorMode,
    strategy: &str,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<String> {
    // NOTE:
    // ErrorMode::Warningを指定している場合は、エラーを吐くようにし、Warningを吐いてからErrorMode::Ignoreにして再度呼び出す
    let rust_strategy = extract_strategy(strategy, kwargs)?;
    let result = kanalizer::convert(word)
        .with_max_length(max_length)
        .with_strategy(&rust_strategy)
        .with_error_on_invalid_input(on_invalid_input != ErrorMode::Ignore)
        .with_error_on_incomplete(on_incomplete != ErrorMode::Ignore)
        .perform();

    // TODO: このmatch文をすっきりさせる
    return match result {
        Ok(dst) => Ok(dst),
        Err(err @ kanalizer::Error::EmptyInput) if on_invalid_input == ErrorMode::Warning => {
            do_warn::<EmptyInputWarning>(py, &err)?;

            convert(
                py,
                word,
                max_length,
                ErrorMode::Ignore,
                on_incomplete,
                strategy,
                kwargs,
            )
        }
        Err(err @ kanalizer::Error::EmptyInput) => Err(EmptyInputError::new_err(err.to_string())),
        Err(err @ kanalizer::Error::InvalidChars { .. })
            if on_invalid_input == ErrorMode::Warning =>
        {
            do_warn::<InvalidCharsWarning>(py, &err)?;

            convert(
                py,
                word,
                max_length,
                ErrorMode::Ignore,
                on_incomplete,
                strategy,
                kwargs,
            )
        }
        Err(ref err @ kanalizer::Error::InvalidChars { ref chars }) => Err(
            InvalidCharsError::new_err((err.to_string(), chars.to_vec())),
        ),
        Err(err @ kanalizer::Error::IncompleteConversion { .. })
            if on_incomplete == ErrorMode::Warning =>
        {
            do_warn::<IncompleteConversionWarning>(py, &err)?;

            convert(
                py,
                word,
                max_length,
                on_invalid_input,
                ErrorMode::Ignore,
                strategy,
                kwargs,
            )
        }
        Err(
            ref err @ kanalizer::Error::IncompleteConversion {
                ref incomplete_output,
            },
        ) => Err(IncompleteConversionError::new_err((
            err.to_string(),
            incomplete_output.to_owned(),
        ))),
    };

    fn do_warn<T: pyo3::PyTypeInfo>(py: Python, err: &kanalizer::Error) -> PyResult<()> {
        let pyerr = py.get_type::<T>();
        let message_cstr =
            std::ffi::CString::new(err.to_string()).expect("should not contain nul byte");
        pyo3::PyErr::warn(py, &pyerr, &message_cstr, 0)
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
