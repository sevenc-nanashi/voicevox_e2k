import voicevox_e2k
from pytest_benchmark.fixture import BenchmarkFixture


def test_c2k():
    c2k = voicevox_e2k.C2k()

    word = "constants"
    assert c2k(word) == "コンスタンツ"


def test_c2k_benchmark(benchmark: BenchmarkFixture):
    c2k = voicevox_e2k.C2k(max_length=128)
    benchmark(c2k, "phosphoribosylaminoimidazolesuccinocarboxamide")
