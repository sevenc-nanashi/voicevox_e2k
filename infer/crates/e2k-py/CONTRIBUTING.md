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
(cd ../e2k-rs && cargo about generate about.hbs.md > ../e2k-py/NOTICE.md)
uv run maturin build --release
```

## テスト

```bash
uv run pytest
```
