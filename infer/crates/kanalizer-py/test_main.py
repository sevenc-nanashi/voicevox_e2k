import kanalizer


def test_c2k():
    kana = kanalizer.Kanalizer()

    word = "kanalizer"
    assert kana.infer(word) == "カナライザー"
