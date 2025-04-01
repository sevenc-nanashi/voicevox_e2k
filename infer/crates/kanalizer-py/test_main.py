import kanalizer


def test_kana():
    kana = kanalizer.Kanalizer()

    word = "kanalizer"
    assert kana.infer(word) == "カナライザー"
