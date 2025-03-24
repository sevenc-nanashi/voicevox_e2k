import voicevox_e2k
from pytest_benchmark.fixture import BenchmarkFixture


def test_c2k():
    c2k = voicevox_e2k.C2k()

    word = "constants"
    assert c2k(word) == "コンスタンツ"


def test_c2k_benchmark(benchmark: BenchmarkFixture):
    print(f"BLAS is {voicevox_e2k.BLAS}")
    c2k = voicevox_e2k.C2k(max_length=128)
    benchmark(c2k, "phosphoribosylaminoimidazolesuccinocarboxamide")
