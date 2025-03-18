"""
Exports the torch weights
"""

import torch
from safetensors.numpy import save_file
import argparse
import brotli
import pathlib
import yaml
from train import Model
from config import Config

parser = argparse.ArgumentParser()

parser.add_argument("--model", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
parser.add_argument("--fp32", action="store_true")

args = parser.parse_args()

config = pathlib.Path(args.model).parent / "config.yml"
config = Config.from_dict(yaml.safe_load(config.open()))
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

output = (
    args.output
    if args.output.endswith(".safetensors")
    else f"{args.output}.safetensors"
)
save_file(weights, output)
with open(output, "rb") as f:
    compressed = brotli.compress(f.read())
with open(output + ".br", "wb") as f:
    f.write(compressed)
