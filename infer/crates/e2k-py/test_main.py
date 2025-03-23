import voicevox_e2k


def test_c2k():
    c2k = voicevox_e2k.C2k()

    word = "constants"
    assert c2k(word) == "コンスタンツ"


def test_c2k_benchmark(benchmark):
    c2k = voicevox_e2k.C2k()
    kata = benchmark(c2k, "constants")
    assert kata == "コンスタンツ"
