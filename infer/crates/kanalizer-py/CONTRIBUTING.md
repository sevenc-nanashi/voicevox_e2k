# 開発者向け

## プロジェクトのセットアップ

[uv](https://docs.astral.sh/uv/)が必要です。

```bash
uv sync
```

## 開発用ビルド

```bash
uv run maturin develop
```

## リリース用ビルド

```bash
cd ../../tools
uv run ./build_kanalizer_py.py
```

## テスト

```bash
uv run pytest
```

## 静的解析

```bash
uv run ruff check 
```

## フォーマット

```bash
uv run ruff format
```
