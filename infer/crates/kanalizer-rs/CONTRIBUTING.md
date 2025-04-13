# 開発者ガイド

## モデルの変更

`./models/model-c2k.safetensors` にモデルを配置するとそのモデルが読み込まれます。

## 開発方針

以下の部分は[Patchethium/e2k](https://github.com/Patchethium/e2k)のコードと可能な限り1:1で対応させるようにしています。

- `./src/layers.rs`：全部分
- `./src/inference.rs`：BaseE2k

## APIの名付け

外部に露出するAPIは「何をしているか」ではなく「何をするか」で名付けるようにしています。\
例えば、`kanalizer::convert`は内部では推論を行っていますが、この関数は「変換する」関数であるため、`convert`と名付けています。
