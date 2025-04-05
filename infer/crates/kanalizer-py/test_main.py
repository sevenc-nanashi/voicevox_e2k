from kanalizer import Kanalizer


def test_kanalizer():
    kanalizer = Kanalizer()

    word = "kanalizer"
    assert kanalizer.convert(word) == "カナライザー"
