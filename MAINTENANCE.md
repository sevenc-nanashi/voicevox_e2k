# メンテナンスガイドライン

## モデル/データセットの更新

モデルやデータセットを更新する場合は、以下の手順に従ってください。

1. Hugging Faceを更新する
  1. [VOICEVOX/e2k](https://huggingface.co/VOICEVOX/e2k)をcloneする。
  2. モデル/データセットの更新を行う。
  3. PRを作成し、マージする。
  4. `git tag v{バージョン番号}`でタグを打つ。
  5. `git push origin v{バージョン番号}`でタグをpushする。
2. Githubを更新する
  1. `infer/crates/e2k-rs/build.rs`の`MODEL_TAG`を更新する。
