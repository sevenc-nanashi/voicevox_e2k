# e2k/train

学習用コードと推論のPython実装です。

## 実行

[uv](https://docs.astral.sh/uv/)、[Task](https://taskfile.dev/) が必要です。

### 学習

```bash
# CPUのみで学習する場合
task train-cpu

# CUDAを使って学習する場合
task train-cuda
```

### 評価

```bash
# UniDicをダウンロードし、英単語を抜き出す（初回のみ）
task setup-eval

# CPUのみで評価する場合
task eval-cpu

# CUDAを使って評価する場合
task eval-cuda
```

## 謝辞

このディレクトリ下のコードは[Patchethium/e2k](https://github.com/Patchethium/e2k)のコードが元になっています。
