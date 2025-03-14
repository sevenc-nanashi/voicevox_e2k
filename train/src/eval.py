# Description: Evaluate the model on the full dataset.
# and calculate the accuracy.
import torch
import argparse
from torcheval.metrics import BLEUScore
from tqdm.auto import tqdm
from train import Model, MyDataset, random_split

parser = argparse.ArgumentParser()

parser.add_argument("--data", type=str, default="./vendor/unidic_words.jsonl")
parser.add_argument("--model", type=str, default="./vendor/model-c2k-e10.pth")
parser.add_argument("--p2k", action="store_true")
parser.add_argument("--portion", type=float, default=1.0)

args = parser.parse_args()

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f"Using device: {device}")

if use_cuda:
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.set_float32_matmul_precision("high")
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True


model = Model(p2k=args.p2k).to(device)

model.load_state_dict(torch.load(args.model, map_location=torch.device("cpu")))

model.eval()

torch.manual_seed(3407)

dataset = MyDataset(args.data, device, p2k=args.p2k)
dataset.set_return_full(True)  # bleu score test
test_ds, _ = random_split(dataset, [args.portion, 1 - args.portion])

bleu = BLEUScore(n_gram=3)


def tensor2str(t):
    return " ".join([str(int(x)) for x in t])


for (eng, kata) in tqdm(test_ds, desc="Evaluating"):
    res = model.inference(eng)
    pred_kana = tensor2str(res)
    kana = [[tensor2str(k) for k in kata]]
    bleu.update(pred_kana, kana)


print(f"BLEU score: {bleu.compute()}")
