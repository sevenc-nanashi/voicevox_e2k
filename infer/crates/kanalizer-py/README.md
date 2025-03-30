# kanalizer

英単語から読みを推論するライブラリ。
[kanalizer](https://github.com/VOICEVOX/kanalizer/tree/main/infer/crates/kanalizer-rs)のPythonバインディングです。

## 使い方

```py
# 文字列をカタカナに変換する例
import kanalizer

c2k = kanalizer.C2k()

word = "kanalizer"
print(c2k(word)) # => カナライザー
```

## ライセンス

MIT License にて公開しています。
Rustで依存しているクレートのライセンスは、生成されるNOTICE.mdを参照してください。
