use thiserror::Error;

#[derive(Error, Debug, Clone, PartialEq)]
pub enum Error {
    #[error("入力が空です")]
    EmptyInput,
    #[error("無効な文字が含まれています：{chars:?}")]
    InvalidChars { chars: Vec<char> },
    #[error("推論が終了しませんでした")]
    InferenceNotFinished { incomplete_output: String },
}

pub type Result<T> = std::result::Result<T, Error>;
