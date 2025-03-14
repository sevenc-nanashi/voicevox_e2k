import torch
from torcheval.metrics import BLEUScore
from tqdm.auto import tqdm


def tensor2str(t):
    return " ".join([str(int(x)) for x in t])


class Evaluator:
    def __init__(self, dataset):
        self.dataset = dataset

    def evaluate(self, model):
        bleu = BLEUScore(n_gram=3)

        with torch.no_grad():
            for eng, kata in tqdm(self.dataset, desc="Evaluating"):
                res = model.inference(eng)
                pred_kana = tensor2str(res)
                kana = [[tensor2str(k) for k in kata]]
                bleu.update(pred_kana, kana)

        return bleu.compute()
