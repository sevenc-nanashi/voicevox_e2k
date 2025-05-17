import pytest

import kanalizer


def test_kanalizer():
    word = "kanalizer"
    assert kanalizer.convert(word) == "カナライザー"


@pytest.mark.parametrize(
    "max_length, exception",
    [
        ("hoge", ValueError),
        (0, ValueError),
        (-42, OverflowError),
        (2**64 + 1, OverflowError),
        (dict(), TypeError),
    ],
)
def test_invalid_max_length(max_length, exception):
    word = "kanalizer"
    with pytest.raises(exception):
        kanalizer.convert(word, max_length=max_length)


def test_empty_word_error():
    word = ""
    with pytest.raises(kanalizer.EmptyInputError):
        kanalizer.convert(word, on_invalid_input="error")


def test_empty_word_warning():
    word = ""
    with pytest.warns(kanalizer.EmptyInputWarning):
        assert kanalizer.convert(word, on_invalid_input="warning") == ""


@pytest.mark.parametrize(
    "word",
    [("あ"), ("A")],
)
def test_invalid_chars_error(word: str):
    with pytest.raises(kanalizer.InvalidCharsError) as ce:
        kanalizer.convert(word, on_invalid_input="error")
    assert ce.value.invalid_chars == [word]


@pytest.mark.parametrize(
    "word",
    [("あ"), ("A")],
)
def test_invalid_chars_warning(word: str):
    with pytest.warns(kanalizer.InvalidCharsWarning):
        kanalizer.convert(word, on_invalid_input="warning")


def test_inference_not_finished_error():
    word = "phosphoribosylaminoimidazolesuccinocarboxamide"
    with pytest.raises(
        kanalizer.IncompleteConversionError,
        match=r'変換が終了しませんでした：".+"',
    ):
        kanalizer.convert(word, max_length=5, on_incomplete="error")


def test_inference_not_finished_warning():
    word = "phosphoribosylaminoimidazolesuccinocarboxamide"
    with pytest.warns(kanalizer.IncompleteConversionWarning):
        kanalizer.convert(word, max_length=5, on_incomplete="warning")
