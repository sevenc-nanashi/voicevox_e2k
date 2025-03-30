import kanalizer


def test_c2k():
    c2k = kanalizer.C2k()

    word = "constants"
    assert c2k(word) == "コンスタンツ"
