import voicevox_e2k


def test_c2k():
    c2k = voicevox_e2k.C2k(voicevox_e2k.MODEL)

    word = "constants"
    assert c2k(word) == "コンスタンツ"
