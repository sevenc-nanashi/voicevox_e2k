from typing import Final, Literal, overload

__version__: Final[str]
"""バージョン。"""

KANAS: Final[list[str]]
"""Kanalizerの入力に使える文字の一覧。"""
ASCII_ENTRIES: Final[list[str]]
"""Kanalizerで出力される文字の一覧。"""

Strategy = Literal["greedy", "top_k", "top_p"]
"""デコードのアルゴリズム。"""

@overload
def convert(
    word: str,
    /,
    *,
    max_length: int = 32,
    strategy: Literal["greedy"] = "greedy",
) -> str: ...
@overload
def convert(
    word: str,
    /,
    *,
    max_length: int = 32,
    strategy: Literal["top_k"],
    k: int = 10,
) -> str: ...
@overload
def convert(
    word: str,
    /,
    *,
    max_length: int = 32,
    strategy: Literal["top_p"],
    p: float = 0.9,
    t: float = 1.0,
) -> str: ...
def convert(
    word: str, /, *, max_length: int = 32, strategy: Strategy = "greedy", **kwargs
) -> str:
    """
    推論を行う。

    Parameters
    ----------
    word : str
        英単語。
    max_length : int, default 32
        最大の出力長。
    validate_input : bool, default True
        入力の検証を行うかどうか。
        Falseの場合、無効な文字が含まれていてもエラーを出しません。
    strategy : Strategy, default "greedy"
        デコードのアルゴリズム。
    k : int, default 10
        strategy="top_k"のときのみ有効。Top-KアルゴリズムのK。
    p : float, default 0.9
        strategy="top_p"のときのみ有効。Top-PアルゴリズムのP。
    t : float, default 1.0
        strategy="top_p"のときのみ有効。Top-PアルゴリズムのTemperature。

    Raises
    ------
    ValueError
        - validate_inputがTrue、かつ`word`が空文字列の場合。
        - validate_inputがTrue、かつ`word`にKanalizerの入力に使えない文字が含まれている場合。
        - `max_length`が0以下の場合。
    """
    ...
