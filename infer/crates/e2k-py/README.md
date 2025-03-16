# e2k-py

英単語から読みを推論するライブラリ。
[e2k](https://github.com/VOICEVOX/e2k/tree/main/infer/crates/e2k-rs)のPythonバインディングです。

## 使い方

```py
# 文字列をカタカナに変換する例
import e2k_rs

c2k = e2k_rs.C2k(e2k_rs.models.MODEL)

word = "constants"
print(c2k(word)) # => コンスタンツ
```

## ライセンス

MIT License にて公開しています。
Rustで依存しているクレートのライセンスはNOTICE.mdを参照してください。
