# voicevox_e2k

英単語から読みを推論するライブラリ。
[e2k](https://github.com/VOICEVOX/e2k/tree/main/infer/crates/e2k-rs)のPythonバインディングです。

## 使い方

```py
# 文字列をカタカナに変換する例
import voicevox_e2k

c2k = voicevox_e2k.C2k()

word = "constants"
print(c2k(word)) # => コンスタンツ
```

## ライセンス

MIT License にて公開しています。
Rustで依存しているクレートのライセンスは、生成されるNOTICE.mdを参照してください。
