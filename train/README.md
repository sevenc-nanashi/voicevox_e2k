# e2k/train

学習用コードと推論のPython実装です。

## 実行

[uv](https://docs.astral.sh/uv/) が必要です。

### 学習

学習結果は `vendor/model-c2k-e10.pth`、`vendor/model-c2k-e10-[label].pth` に保存されます。

```bash
# 学習
uv run python3 train.py --label [label]
```

```bash
# Tensorboardを開く
uv run tensorboard --logdir runs
```

### データセットの結合

```bash
uv run python3 merge.py ./vendor/dataset_01.jsonl ./vendor/dataset_02.jsonl --output ./vendor/dataset_merged.jsonl
```

### 評価

評価はデフォルトではUniDicの英単語を使って行います。
別の辞書を使いたい場合は、`--data` オプションで指定してください。
データセットの一部分のみに対して評価を行いたい場合は、`--portion` オプションで割合を指定してください。

```bash
# UniDicをダウンロードし、英単語を抜き出す（初回のみ）
uv run python3 setup_eval.py
```

```bash
# 評価
uv run python3 eval.py
```

### 書き出し

safetensors形式で書き出します。

```bash
uv run python3 export.py --model ./vendor/model-c2k-e10.pth --output ../infer/crates/e2k-rs/src/models/model-c2k.safetensors
```

### フォーマット

```bash
uv run ruff check *.py

uv run ruff format *.py
```

## 謝辞

このディレクトリ下のコードは[Patchethium/e2k](https://github.com/Patchethium/e2k)のコードが元になっています。
