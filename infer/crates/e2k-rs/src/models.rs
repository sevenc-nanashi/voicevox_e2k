macro_rules! model {
    ($model_path:literal) => {
        std::sync::LazyLock::new(|| {
            cfg_elif::expr::cfg!(if (docsrs) {
                Vec::new()
            } else if (feature == "compress_model") {
                {
                    use std::io::Read;
                    let model = include_bytes!(concat!("./models/", $model_path, ".br"));
                    let mut input = brotli_decompressor::Decompressor::new(model.as_slice(), 4096);
                    let mut buf = Vec::new();
                    input.read_to_end(&mut buf).expect("Model is corrupted");
                    buf
                }
            } else {
                include_bytes!(concat!("./models/", $model_path))
            })
        })
    };
}

/// [crate::C2k]のモデル。
pub static C2K_MODEL: std::sync::LazyLock<Vec<u8>> = model!("model-c2k.safetensors");

/// [crate::P2k]のモデル。
pub static P2K_MODEL: std::sync::LazyLock<Vec<u8>> = model!("model-p2k.safetensors");
