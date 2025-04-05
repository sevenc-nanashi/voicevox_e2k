# kanalizer

推論コードのRust実装。

## 使い方

```rust
// 文字列をカタカナに変換する例
let src = "kanalizer";
let kanalizer = kanalizer::Kanalizer::new();
let dst = kanalizer.convert(src);

assert_eq!(dst, "カナライザー");
```

## ライセンス

MIT License にて公開しています。
