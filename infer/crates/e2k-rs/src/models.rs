/// [crate::C2k]のモデル。
pub static MODEL: std::sync::LazyLock<Vec<u8>> = std::sync::LazyLock::new(|| {
    cfg_elif::expr::cfg!(if (docsrs) {
        Vec::new()
    } else if (feature == "compress_model") {
        {
            use std::io::Read;
            let model =
                include_bytes!(concat!(env!("E2K_MODEL_ROOT"), "/model-c2k.safetensors.br"));
            let mut input = brotli_decompressor::Decompressor::new(model.as_slice(), 4096);
            let mut buf = Vec::new();
            input.read_to_end(&mut buf).expect("Model is corrupted");
            buf
        }
    } else {
        include_bytes!(concat!(env!("E2K_MODEL_ROOT"), "/model-c2k.safetensors")).to_vec()
    })
});
