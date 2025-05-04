"""
英単語列からカタカナ列を推論するスクリプト。
- 引数に単語を指定するとtrainデータと同じjsonl形式で出力する。
  各単語ごとに {"word": ..., "kata": [...]} 形式のjsonを1行ずつ標準出力する。
- 引数に単語を指定しない場合はREPLモードで動作する。

例:
    uv run src/infer.py ./outputs/2025_03_14_23_43_01_example
    uv run src/infer.py ./outputs/2025_03_14_23_43_01_example kanalizer neovim
"""

import argparse
import json
from pathlib import Path

import torch
import yaml
from config import Config
from constants import EOS_IDX, SOS_IDX, kanas

from train import Model, word_to_tensor


def main():
    args = parse_args()
    device = get_device()
    config = load_config(args.model_path.parent)
    model = load_model(args.model_path, config, device)
    words = args.words
    if not words:
        repl_main(model, device)
    else:
        infer_main(model, words, device)


def infer_main(model: Model, words: list[str], device: torch.device):
    for word in words:
        src_tensor = word_to_tensor(word, device)
        katakana = infer_katakana(model, src_tensor)
        obj = {"word": word, "kata": ["".join(katakana)]}
        print(json.dumps(obj, ensure_ascii=False))


def repl_main(model: Model, device: torch.device):
    print("Ctrl+C or empty input to exit.")
    while True:
        word = input("Enter a word: ")
        if not word:
            break
        src_tensor = word_to_tensor(word, device)
        katakana = infer_katakana(model, src_tensor)
        print(f"Katakana: {''.join(katakana)}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", type=Path, help="Path to the model file")
    parser.add_argument("words", nargs="*", help="Input word(s) to infer")
    return parser.parse_args()


def get_device():
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    if use_cuda:
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.set_float32_matmul_precision("high")
        torch.backends.cudnn.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
    return device


def load_config(output_dir: Path) -> Config:
    config_path = output_dir / "config.yml"
    config = Config.from_dict(yaml.safe_load(config_path.read_text()))
    return config


def load_model(model_path: Path, config: Config, device: torch.device) -> Model:
    model = Model(config)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def infer_katakana(model: Model, src_tensor: torch.Tensor) -> list[str]:
    res = model.inference(src_tensor)
    return [kanas[i] for i in res if i != SOS_IDX and i != EOS_IDX]


if __name__ == "__main__":
    main()
