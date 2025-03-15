use std::path::{Path, PathBuf};

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-env-changed=CARGO_FEATURE_EMBED_MODEL");
    if std::env::var("CARGO_FEATURE_EMBED_MODEL") == Ok("1".to_string()) {
        download_models();
    }
}

fn download_models() {
    println!("cargo:rerun-if-changed=models/model-c2k.safetensors");
    println!("cargo:rerun-if-changed=models/model-c2k.safetensors.br");

    let model_exists = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap())
        .join("./models/model-c2k.safetensors")
        .try_exists()
        .unwrap();

    let model_root = if !model_exists {
        let model_root = PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("models");
        std::fs::create_dir_all(&model_root).unwrap();

        if !model_root
            .join("model-c2k.safetensors")
            .try_exists()
            .unwrap()
        {
            download_to(
                "https://github.com/Patchethium/e2k/releases/download/0.3.0/model-c2k.safetensors",
                &model_root.join("model-c2k.safetensors"),
            );
        }
        if !model_root
            .join("model-c2k.safetensors.br")
            .try_exists()
            .unwrap()
        {
            compress_model(&model_root.join("model-c2k.safetensors"));
        }

        model_root
    } else {
        PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap()).join("./models")
    };

    println!("cargo:rustc-env=E2K_MODEL_ROOT={}", model_root.display());
}

fn download_to(url: &str, path: &Path) {
    let response = ureq::get(url).call().unwrap().into_body();
    let temp_path = path.with_extra_extension("tmp");
    let mut file = std::fs::File::create(&temp_path).unwrap();
    std::io::copy(&mut response.into_reader(), &mut file).unwrap();
    std::fs::rename(&temp_path, path).unwrap();
}

fn compress_model(path: &Path) {
    let mut input = std::fs::File::open(path).unwrap();
    let mut output = std::fs::File::create(path.with_extra_extension("br.tmp")).unwrap();
    let mut output_writer = brotli::CompressorWriter::new(&mut output, 4096, 11, 22);
    std::io::copy(&mut input, &mut output_writer).unwrap();
    drop(output_writer);
    std::fs::rename(
        path.with_extra_extension("br.tmp"),
        path.with_extra_extension("br"),
    )
    .unwrap();
}

trait AddExtensionExt {
    fn with_extra_extension(&self, ext: &str) -> PathBuf;
}

impl AddExtensionExt for Path {
    fn with_extra_extension(&self, ext: &str) -> PathBuf {
        self.with_file_name(format!(
            "{}.{}",
            self.file_name().unwrap().to_str().unwrap(),
            ext
        ))
    }
}
