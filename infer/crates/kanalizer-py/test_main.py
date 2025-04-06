import kanalizer


def test_kanalizer():
    word = "kanalizer"
    assert kanalizer.convert(word) == "カナライザー"
