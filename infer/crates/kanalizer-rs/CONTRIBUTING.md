# 開発者ガイド

## モデルの変更

`./models/model-c2k.safetensors` にモデルを配置するとそのモデルが読み込まれます。

## 開発方針

以下の部分は[Patchethium/e2k](https://github.com/Patchethium/e2k)のコードと可能な限り1:1で対応させるようにしています。

- `./src/layers.rs`：全部分
- `./src/inference.rs`：BaseE2k
