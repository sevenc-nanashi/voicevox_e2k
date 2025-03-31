import kanalizer


def test_c2k():
    c2k = kanalizer.C2k()

    word = "kanalizer"
    assert c2k(word) == "カナライザー"
