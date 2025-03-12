# e2k-rs

推論コードのRust実装。

## 使い方

```rust
// 文字列をカタカナに変換する例
let src = "constants";
let c2k = e2k::C2k::new(32);
let dst = c2k.infer(src);

dbg!(dst); // "コンスタンツ"
```

```rust
// CMUDictの発音記号をカタカナに変換する例
let pronunciation = ["K", "AA1", "N", "S", "T", "AH0", "N", "T", "S"];
let p2k = e2k::P2k::new(32);
let dst = p2k.infer(&pronunciation);
dbg!(dst); // "コンスタンツ"
```

## ライセンス

MIT License にて公開しています。
