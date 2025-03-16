import e2k_rs


def test_c2k():
    c2k = e2k_rs.C2k(e2k_rs.MODEL)

    word = "constants"
    assert c2k(word) == "コンスタンツ"
