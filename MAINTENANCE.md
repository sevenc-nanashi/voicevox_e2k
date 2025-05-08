# メンテナンスガイドライン

## データセットの更新

データセットを更新する場合は、以下の手順に従ってください。

1. Hugging Faceを更新する
   1. [VOICEVOX/kanalizer-dataset](https://huggingface.co/datasets/VOICEVOX/kanalizer-dataset)をcloneする。
   2. データセットの更新を行う。
   3. PRを作成し、マージする。
   4. `git tag v{バージョン番号}`でタグを打つ。
   5. `git push origin v{バージョン番号}`でタグをpushする。
2. 必要に応じて、モデルの学習を回す。

## モデルの更新

モデルを更新する場合は、以下の手順に従ってください。

1. Hugging Faceを更新する
   1. [VOICEVOX/kanalizer-model](https://huggingface.co/VOICEVOX/kanalizer-model)をcloneする。
   2. モデルの更新を行う。
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

## モデルの選択基準

kanalizerのモデルは以下の基準で選択されます。

- Loss/evalが小さいもの
- 3文字以下のすべてのアルファベット列で文字数オーバーしないもの
  - このリストはRubyで`("a".."zzz").to_a`を使って作成しています。
