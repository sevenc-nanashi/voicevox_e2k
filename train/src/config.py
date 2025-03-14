from dataclasses import dataclass
import yaml


@dataclass
class Config:
    train_data: str
    eval_data: str
    eval_data_portion: float
    dim: int
    max_epochs: int
    num_models_to_keep: int
    seed: int

    @classmethod
    def load(cls, path: str):
        with open(path, "r") as file:
            config = yaml.safe_load(file)
        return cls(**config)
