//! # kanalizer-rs
//!
//! [Patchethium氏のe2k](https://github.com/Patchethium/e2k)をRustに移植したものです。
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

mod inference;
mod layers;

use std::{num::NonZero, sync::LazyLock};

pub use inference::*;

static KANALIZER: LazyLock<Kanalizer> = LazyLock::new(Kanalizer::new);

/// 推論を行うためのオプションを指定する構造体。
pub struct ConvertBuilder {
    word: String,
    options: ConvertOptions,
}

impl ConvertBuilder {
    fn new(word: &str) -> Self {
        Self {
            word: word.to_string(),
            options: ConvertOptions::default(),
        }
    }

    /// デコードの最大長を指定する。
    pub fn with_max_length(mut self, max_length: NonZero<usize>) -> Self {
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
        KANALIZER.convert(&self.word, &self.options)
    }
}

/// 推論を行う。
pub fn convert(word: &str) -> ConvertBuilder {
    ConvertBuilder::new(word)
}
