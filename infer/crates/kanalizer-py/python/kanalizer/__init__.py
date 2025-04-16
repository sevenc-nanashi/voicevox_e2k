from typing import TYPE_CHECKING
from ._rust import __version__, convert, INPUT_CHARS, OUTPUT_CHARS
from ._error import (
    IncompleteConversionError,
    InvalidInputError,
    EmptyInputError,
    InvalidCharsError,
    IncompleteConversionWarning,
    InvalidInputWarning,
    EmptyInputWarning,
    InvalidCharsWarning,
)

if TYPE_CHECKING:
    from ._rust import Strategy, ErrorMode

__all__ = [
    "__version__",
    "convert",
    "INPUT_CHARS",
    "OUTPUT_CHARS",
    "IncompleteConversionError",
    "InvalidInputError",
    "EmptyInputError",
    "InvalidCharsError",
    "IncompleteConversionWarning",
    "InvalidInputWarning",
    "EmptyInputWarning",
    "InvalidCharsWarning",
    "Strategy",
    "ErrorMode",
]
