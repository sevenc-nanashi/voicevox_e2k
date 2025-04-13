# kanalizer

英単語から読みへの変換を行うライブラリ。\
[kanalizer](https://github.com/VOICEVOX/kanalizer/tree/main/infer/crates/kanalizer-rs)のPythonバインディングです。

## 使い方

```py
# 文字列をカタカナに変換する例
import kanalizer

word = "kanalizer"
print(kanalizer.convert(word)) # => カナライザー
```

## ライセンス

MIT License にて公開しています。
Rustで依存しているクレートのライセンスは、生成されるNOTICE.mdを参照してください。
