# e2k/train

学習用コードと推論のPython実装です。

## 実行

[uv](https://docs.astral.sh/uv/)、[Task](https://taskfile.dev/) が必要です。

### 学習

学習結果は `vendor/model-c2k-e10.pth`、`vendor/model-c2k-e10-[label].pth` に保存されます。

```bash
# CPUのみで学習する場合
task train-cpu -- --label [label]

# CUDAを使って学習する場合
task train-cuda -- --label [label]

# tensorboardを開く
task tensorboard
```

### データセットの結合

```bash
task merge -- ./vendor/dataset_01.jsonl ./vendor/dataset_02.jsonl --output ./vendor/dataset_merged.jsonl
```

### 評価

評価はデフォルトではUniDicの英単語を使って行います。
別の辞書を使いたい場合は、`--data` オプションで指定してください。
データセットの一部分のみに対して評価を行いたい場合は、`--portion` オプションで割合を指定してください。

```bash
# UniDicをダウンロードし、英単語を抜き出す（初回のみ）
task setup-eval

# CPUのみで評価する場合
task eval-cpu -- --model ./vendor/model-c2k-e10.pth

# CUDAを使って評価する場合
task eval-cuda -- --model ./vendor/model-c2k-e10.pth
```

### 書き出し

safetensors形式で書き出します。

```bash
task export -- --model ./vendor/model-c2k-e10.pth --output ../infer/crates/e2k-rs/src/models/model-c2k.safetensors
```

### フォーマット

```bash
task lint

task format
```

## 謝辞

このディレクトリ下のコードは[Patchethium/e2k](https://github.com/Patchethium/e2k)のコードが元になっています。
