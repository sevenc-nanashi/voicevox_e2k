from pathlib import Path
import platform

infer_root = Path(__file__).parent.parent

is_windows = platform.system() == "Windows"
is_linux = platform.system() == "Linux"
