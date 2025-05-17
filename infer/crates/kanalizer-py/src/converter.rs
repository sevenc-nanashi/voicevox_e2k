use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::str::FromStr;
use strum::VariantNames;

pub fn extract_strategy(
    strategy: &str,
    kwargs: Option<&Bound<'_, PyDict>>,
) -> PyResult<kanalizer::Strategy> {
    return Ok(match strategy {
        "greedy" => {
            error_on_extra_args(kwargs, &[])?;

            kanalizer::Strategy::Greedy
        }
        "top_k" => {
            error_on_extra_args(kwargs, &["k"])?;

            let k = kwargs
                .map(|kwargs| kwargs.get_item("k"))
                .transpose()?
                .flatten()
                .map(|k| k.extract::<usize>())
                .transpose()?;

            let mut strategy = kanalizer::StrategyTopK::default();
            if let Some(k) = k {
                strategy.k = k;
            }

            kanalizer::Strategy::TopK(strategy)
        }
        "top_p" => {
            error_on_extra_args(kwargs, &["p", "t"])?;

            let top_p = kwargs
                .map(|kwargs| kwargs.get_item("p"))
                .transpose()?
                .flatten()
                .map(|top_p| top_p.extract::<f32>())
                .transpose()?;

            let temperature = kwargs
                .map(|kwargs| kwargs.get_item("t"))
                .transpose()?
                .flatten()
                .map(|temperature| temperature.extract::<f32>())
                .transpose()?;

            let mut strategy = kanalizer::StrategyTopP::default();
            if let Some(top_p) = top_p {
                strategy.top_p = top_p;
            }
            if let Some(temperature) = temperature {
                strategy.temperature = temperature;
            }

            kanalizer::Strategy::TopP(strategy)
        }
        _ => {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "strategy must be one of 'greedy', 'top_k', 'top_p'",
            ));
        }
    });

    fn error_on_extra_args(kwargs: Option<&Bound<'_, PyDict>>, expected: &[&str]) -> PyResult<()> {
        if let Some(kwargs) = kwargs {
            let keys = kwargs.iter().map(|item| item.0).collect::<Vec<_>>();
            let keys = keys
                .iter()
                .map(|key| key.extract::<String>())
                .collect::<Result<Vec<_>, _>>()?;

            let extra_keys = keys
                .iter()
                .map(|key| key.as_str())
                .filter(|&key| !expected.contains(&key))
                .collect::<Vec<_>>();

            if !extra_keys.is_empty() {
                return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                    "unexpected keyword argument(s): {}",
                    extra_keys.join(", ")
                )));
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Eq, PartialEq, strum::EnumString, strum::Display, strum::VariantNames)]
#[strum(serialize_all = "snake_case")]
pub enum ErrorMode {
    Error,
    Warning,
    Ignore,
}

impl pyo3::FromPyObject<'_> for ErrorMode {
    fn extract_bound(ob: &Bound<'_, PyAny>) -> PyResult<Self> {
        let s: String = ob.extract()?;
        ErrorMode::from_str(&s).map_err(|_| {
            pyo3::exceptions::PyValueError::new_err(format!(
                "Invalid error mode: {}. Must be one of '{}'",
                s,
                ErrorMode::VARIANTS
                    .iter()
                    .map(|s| s.to_string())
                    .collect::<Vec<_>>()
                    .join("', '")
            ))
        })
    }
}

pub fn extract_max_length(ob: &Bound<'_, PyAny>) -> PyResult<kanalizer::MaxLength> {
    return if ob.is_instance_of::<pyo3::types::PyString>() {
        extract_auto(ob)
    } else if ob.is_instance_of::<pyo3::types::PyInt>() {
        extract_integer(ob)
    } else {
        return Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "expected positive int or \"auto\", got {}",
            ob.get_type().name()?
        )));
    };

    fn extract_auto(ob: &Bound<'_, PyAny>) -> PyResult<kanalizer::MaxLength> {
        let value: String = ob.extract()?;
        if value == "auto" {
            Ok(kanalizer::MaxLength::Auto)
        } else {
            Err(pyo3::exceptions::PyValueError::new_err(format!(
                "expected \"auto\", got {value:?}",
            )))
        }
    }
    fn extract_integer(ob: &Bound<'_, PyAny>) -> PyResult<kanalizer::MaxLength> {
        let value: usize = ob.extract()?;
        value.try_into().map_err(|_| {
            pyo3::exceptions::PyValueError::new_err(
                format!("expected positive int, got {value:?}",),
            )
        })
    }
}
