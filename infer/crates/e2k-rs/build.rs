use std::path::{Path, PathBuf};

static MODEL_TAG: &str = "v1";

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    download_models();
}

fn download_models() {
    println!("cargo:rerun-if-changed=models/model-c2k.safetensors");
    println!("cargo:rerun-if-changed=models/model-c2k.safetensors.br");

    let override_model_path = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap())
        .join("./models/model-c2k.safetensors");

    let model_root = if override_model_path.try_exists().unwrap() {
        let compressed_path = override_model_path.with_extra_extension("br");
        if !compressed_path.try_exists().unwrap() {
            compress_model(&override_model_path);
        }

        override_model_path.parent().unwrap().to_path_buf()
    } else {
        let model_root = PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("models");
        std::fs::create_dir_all(&model_root).unwrap();

        let model_version_path = PathBuf::from(std::env::var("OUT_DIR").unwrap())
            .join("models")
            .join("version.txt");

        let latest_model_exists = model_version_path
            .try_exists()
            .unwrap()
            .then(|| std::fs::read_to_string(&model_version_path).unwrap())
            .as_deref()
            == Some(MODEL_TAG);

        if !latest_model_exists {
            download_to(
                &format!(
                    "https://huggingface.co/VOICEVOX/e2k/resolve/{MODEL_TAG}/model/c2k.safetensors"
                ),
                &model_root.join("model-c2k.safetensors"),
            );

            compress_model(&model_root.join("model-c2k.safetensors"));

            std::fs::write(&model_version_path, MODEL_TAG).unwrap();
        }

        model_root
    };

    println!("cargo:rustc-env=E2K_MODEL_ROOT={}", model_root.display());
}

fn download_to(url: &str, path: &Path) {
    let response = ureq::get(url).call().unwrap();
    let temp_path = path.with_extra_extension("tmp");
    let mut file = std::fs::File::create(&temp_path).unwrap();
    std::io::copy(&mut response.into_body().into_reader(), &mut file).unwrap();
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
