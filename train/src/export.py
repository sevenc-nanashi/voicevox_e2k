"""
Exports the torch weights
"""

import torch
from safetensors.numpy import save_file as save_safetensors
import argparse
from pathlib import Path
import yaml
from train import Model
from config import Config

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

save_safetensors(weights, args.output)
