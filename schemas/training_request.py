from pydantic import BaseModel
from typing import Optional, Dict

class TrainingArguments(BaseModel):
    lr: float
    optim: str
    gpus: int
    steps: int

class DataConfig(BaseModel):
    collection: str
    process_script: str
    dataset_class: str

class TrainingConfig(BaseModel):
    method: str
    training_arguments: TrainingArguments
    algorithm: str
    scoring_script: str
    scoring_class: str

class OutputConfig(BaseModel):
    save_chks_path: str
    sync_with_samplers: bool

class TrainingRequest(BaseModel):
    model_name_or_path: str
    data_config: DataConfig
    training_config: TrainingConfig
    output_config: OutputConfig