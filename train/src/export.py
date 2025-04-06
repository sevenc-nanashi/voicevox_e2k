"""
Exports the torch weights
"""

import argparse
from pathlib import Path

from safetensors.numpy import save_file as save_safetensors
import torch
import yaml

from config import Config
from constants import kanas, ascii_entries, SOS_IDX, EOS_IDX
from train import Model

parser = argparse.ArgumentParser()

parser.add_argument("--fp32", action="store_true")
parser.add_argument("--model", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--config", type=Path, required=False)

args = parser.parse_args()

if args.config is None:
    config = args.model.parent / "config.yml"
else:
    config = args.config

config = Config.from_dict(yaml.safe_load(config.read_text()))
model = Model(config)
model.load_state_dict(torch.load(args.model))
model.eval()

if not args.fp32:
    model = model.half()

weights = {}

for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.data.shape)
        weights[name] = param.data.cpu().numpy()

print(f"Saving to {args.output}")

save_safetensors(
    weights,
    args.output,
    # NOTE: Metadataはdict[str, str]である必要がある。
    # そのため、
    # - list[str]はnull文字区切りで結合する。
    # - intはstrに変換する。
    metadata={
        "in_table": "\x00".join(ascii_entries),
        "out_table": "\x00".join(kanas),
        "sos_idx": str(SOS_IDX),
        "eos_idx": str(EOS_IDX),
    },
)
