from pathlib import Path
from typing import Final
import platform

repo_root: Final[Path] = Path(__file__).parent.parent.parent
infer_root: Final[Path] = repo_root / "infer"
train_root: Final[Path] = repo_root / "train"

# pyrightはelif内もFinalへの再代入として認識するため、Finalを外した変数を用意してそれをFinalに代入する
_os_name: str

if platform.system() == "Windows":
    _os_name = "windows"
elif platform.system() == "Linux":
    _os_name = "linux"
elif platform.system() == "Darwin":
    _os_name = "macos"
else:
    raise RuntimeError(f"Unsupported platform: {platform.system()}")

os_name: Final[str] = _os_name

is_windows: Final[bool] = os_name == "windows"
is_linux: Final[bool] = os_name == "linux"
