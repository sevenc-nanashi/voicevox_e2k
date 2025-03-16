from typing import Final, Literal, overload

KANAS: Final[list[str]]
ASCII_ENTRIES: Final[list[str]]
MODEL: Final[bytes]

class C2k:
    """英単語 -> カタカナの推論を行う。"""

    def __init__(self, model: bytes, *, max_len: int = 32) -> None:
        """
        新しいインスタンスを生成する。

        Parameters
        ----------
        model : bytes
            モデルのバイナリデータ。
        max_len : int, default 32
            最大の入力長。
        """

        ...

    @overload
    def set_decode_strategy(self, strategy: Literal["greedy"]) -> None: ...
    @overload
    def set_decode_strategy(self, strategy: Literal["top_k"], k: int) -> None: ...
    @overload
    def set_decode_strategy(
        self, strategy: Literal["top_p"], p: float, t: float
    ) -> None: ...
    def set_decode_strategy(self, strategy: str, **kwargs) -> None:
        """
        デコード戦略を設定する。

        Parameters
        ----------
        strategy : str
            デコード戦略。
        **kwargs
            戦略に応じた引数。詳細はメソッドのオーバーロードを参照。
        """
        ...

    def __call__(self, word: str) -> str:
        """
        推論を行う。

        Parameters
        ----------
        word : str
            英単語。

        Returns
        -------
        str
            カタカナ。
        """
        ...
