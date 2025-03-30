from pathlib import Path
import platform

repo_root = Path(__file__).parent.parent.parent
infer_root = repo_root / "infer"
train_root = repo_root / "train"

is_windows = platform.system() == "Windows"
is_linux = platform.system() == "Linux"
