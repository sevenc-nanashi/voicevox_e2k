from dataclasses import dataclass


def migrate(config: dict):
    # num_models_to_keepをnum_last_models_to_keepとnum_best_models_to_keepに分割
    if "num_models_to_keep" in config:
        config["num_last_models_to_keep"] = config["num_models_to_keep"]
        config["num_best_models_to_keep"] = config["num_models_to_keep"]
        del config["num_models_to_keep"]

    if "optimizer_lr" not in config:
        config["optimizer_lr"] = 1e-3

    if "exponential_lr_scheduler_gamma" in config:
        del config["exponential_lr_scheduler_gamma"]

    if "use_layernorm" not in config:
        config["use_layernorm"] = False

    if "weight_decay" not in config:
        config["weight_decay"] = 0

    if "eval_data" in config:
        del config["eval_data"]

    if "eval_max_words" in config:
        del config["eval_max_words"]

    return config


@dataclass
class Config:
    train_data: str
    eval_ratio: float
    dim: int
    max_epochs: int
    num_last_models_to_keep: int
    num_best_models_to_keep: int
    seed: int
    optimizer_lr: float
    use_layernorm: bool
    weight_decay: float

    @classmethod
    def from_dict(cls, config: dict):
        return cls(**migrate(config))
