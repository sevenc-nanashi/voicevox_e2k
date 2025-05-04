# Description: Evaluate the model on the full dataset.
# and calculate the accuracy.
import sys
import torch
import yaml
from pathlib import Path
from config import Config
from evaluator import Evaluator
from train import Model, MyDataset

if len(sys.argv) < 2:
    print("Usage: python eval.py model")
    sys.exit(1)


model_path = Path(sys.argv[1])

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f"Using device: {device}")

if use_cuda:
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.set_float32_matmul_precision("high")
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True


config = Config.from_dict(
    yaml.safe_load((model_path.parent / "config.yml").read_text())
)

model = Model(config)
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

dataset = MyDataset(config.eval_data, device, max_words=None)
dataset.set_return_full(True)  # bleu score test

evaluator = Evaluator(dataset)

print(f"BLEU score: {evaluator.evaluate(model)}")
