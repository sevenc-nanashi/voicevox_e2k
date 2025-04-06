//! # kanalizer-rs
//!
//! [Patchethium氏のkanalizer](https://github.com/Patchethium/kanalizer)をRustに移植したものです。
//!
//! ## 使い方
//!
//! ```rust
//! // 文字列をカタカナに変換する例
//! let src = "kanalizer";
//! let dst = kanalizer::convert(src).perform();
//!
//! assert_eq!(dst, "カナライザー");
//! ```
//!
//! ## Features
//! ### `compress_model`
//! brotliを使用してモデルを圧縮します。
//! このfeatureはデフォルトで有効です。
//!
//! ### `getrandom_on_wasm32_unknown`
//! wasm32-unknown-unknownでのTopK/TopPサンプリングに`getrandom`を使用します。
//! このfeatureを有効にしてコンパイルするには[getrandomのドキュメント](https://docs.rs/getrandom/latest/getrandom/#webassembly-support)を参照してください。
//! オフの場合、Hashと適当な値を使用してサンプリングします。
//!

mod constants;
mod inference;
mod layers;

use std::sync::LazyLock;

pub use constants::{ASCII_ENTRIES, KANAS};
pub use inference::*;

static KANALIZER: LazyLock<Kanalizer> = LazyLock::new(Kanalizer::new);

pub struct ConvertBuilder {
    input: String,
    options: ConvertOptions,
}

impl ConvertBuilder {
    fn new(input: &str) -> Self {
        Self {
            input: input.to_string(),
            options: ConvertOptions::default(),
        }
    }

    /// デコードの最大長を指定する。
    pub fn with_max_length(mut self, max_length: usize) -> Self {
        self.options.max_length = max_length;
        self
    }

    /// デコードに使うアルゴリズムを指定する。
    pub fn with_strategy(mut self, strategy: &Strategy) -> Self {
        self.options.strategy = strategy.clone();
        self
    }

    /// 推論を行う。
    pub fn perform(self) -> String {
        KANALIZER.convert(&self.input, &self.options)
    }
}

/// 推論を行う。
pub fn convert(input: &str) -> ConvertBuilder {
    ConvertBuilder::new(input)
}
