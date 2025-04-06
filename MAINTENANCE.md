# メンテナンスガイドライン

## モデル/データセットの更新

モデルやデータセットを更新する場合は、以下の手順に従ってください。

1. Hugging Faceを更新する
  1. [VOICEVOX/kanalizer](https://huggingface.co/VOICEVOX/kanalizer)をcloneする。
  2. モデル/データセットの更新を行う。
  3. PRを作成し、マージする。
  4. `git tag v{バージョン番号}`でタグを打つ。
  5. `git push origin v{バージョン番号}`でタグをpushする。
2. Githubを更新する
  1. `infer/crates/kanalizer-rs/build.rs`の`MODEL_TAG`を更新する。

## リリース先の方針

- リリース時の挙動を確認したいときはTestPyPIに上げる。
- メインPyPIはプレリリース（rc）含めユーザーが使っていいものにする。
- GitHubのReleases下はメインPyPIと同じようにする。

## PyPIの管理

- メインPyPIのkanalizerは[VOICEVOX Org](https://pypi.org/org/VOICEVOX/)で管理しています。
- TestPyPIのkanalizerは[@sevenc-nanashi](https://test.pypi.org/user/sevenc-nanashi/)が管理しています。
