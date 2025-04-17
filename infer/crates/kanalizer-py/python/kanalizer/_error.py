class IncompleteConversionError(Exception):
    """
    変換が終了しなかった場合に発生するエラー。

    Attributes
    ----------
    incomplete_output : str
        不完全な出力。
    """

    incomplete_output: str

    def __init__(self, message: str, incomplete_output: str):
        super().__init__(message)
        self.incomplete_output = incomplete_output


class InvalidInputError(ValueError):
    """
    無効な入力が与えられた場合に発生するエラーの基底クラス。

    See Also
    --------
    InvalidCharsError
        無効な文字が含まれている場合に発生するエラー。
    EmptyInputError
        入力が空文字列の場合に発生するエラー。
    """


class EmptyInputError(InvalidInputError):
    """
    入力が空文字列の場合に発生するエラー。
    """


class InvalidCharsError(InvalidInputError):
    """
    入力に無効な文字が含まれていた場合に発生するエラー。

    Attributes
    ----------
    invalid_chars : list[str]
        無効な文字。
    """

    def __init__(self, message: str, invalid_chars: list[str]):
        super().__init__(message)
        self.invalid_chars = invalid_chars


class IncompleteConversionWarning(Warning):
    """
    変換が終了しなかった場合に発生する警告。

    IncompleteConversionErrorとは異なり、incomplete_output属性は存在しない。
    """


class InvalidInputWarning(Warning):
    """
    無効な入力が与えられた場合に発生する警告の基底クラス。

    See Also
    --------
    InvalidCharsWarning
        無効な文字が含まれている場合に発生する警告。
    EmptyInputWarning
        入力が空文字列の場合に発生する警告。
    """


class EmptyInputWarning(InvalidInputWarning):
    """
    入力が空文字列の場合に発生する警告。
    """


class InvalidCharsWarning(InvalidInputWarning):
    """
    入力に無効な文字が含まれていた場合に発生する警告。

    InvalidCharsErrorとは異なり、invalid_chars属性は存在しない。
    """

    def __init__(self, message: str):
        super().__init__(message)
