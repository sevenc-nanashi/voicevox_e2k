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

mod constants;
mod inference;
mod layers;

use std::{collections::HashSet, num::NonZero, sync::LazyLock};

pub use inference::*;
use itertools::Itertools;

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

/// Kanalizerの入力に使える文字の一覧。
pub static INPUT_CHARS: LazyLock<HashSet<char>> = LazyLock::new(|| {
    constants::KANAS
        .iter()
        .flat_map(|s| {
            let c = s.chars().exactly_one();
            if c.is_err() {
                // 制御文字は除外
                assert!(
                    s.starts_with('<') && s.ends_with('>'),
                    "unexpected character: {s:?}",
                );
            }
            c
        })
        .collect()
});

/// Kanalizerから出力されうる文字の一覧。
pub static OUTPUT_CHARS: LazyLock<HashSet<char>> = LazyLock::new(|| {
    constants::ASCII_ENTRIES
        .iter()
        .flat_map(|s| {
            let c = s.chars().exactly_one();
            if c.is_err() {
                // 制御文字は除外
                assert!(
                    s.starts_with('<') && s.ends_with('>'),
                    "unexpected character: {s:?}",
                );
            }
            c
        })
        .collect()
});
