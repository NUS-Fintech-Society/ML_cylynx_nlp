from pydantic import BaseModel
import yaml
import os
from pathlib import Path


class ModelConfig(BaseModel):
    ner_model_path: str
    sent_model_path: str


class Config(BaseModel):
    model_config: ModelConfig
    db_path: str


def load_config(cfg_path):
    cfg_dict = yaml.load(open(cfg_path), yaml.Loader)
    model_config = ModelConfig(**cfg_dict["model_config"])
    config = Config(model_config=model_config,
                    db_path=cfg_dict["db_path"])
    return config


root_dir = Path(__file__).parent.parent
config_file_path = Path.joinpath(root_dir,"cfg.yaml")

config = load_config(config_file_path)
