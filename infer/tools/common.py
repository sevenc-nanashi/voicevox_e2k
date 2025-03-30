from pathlib import Path
from typing import Final
import platform

repo_root: Final[Path] = Path(__file__).parent.parent.parent
infer_root: Final[Path] = repo_root / "infer"
train_root: Final[Path] = repo_root / "train"

is_windows: Final[bool] = platform.system() == "Windows"
is_linux: Final[bool] = platform.system() == "Linux"
