from schemas.training_request import TrainingRequest
from services.config_builder import build_training_config
from services.trainer_factory import get_trainer
from utils.logger import logger

def start_training_task(request: TrainingRequest):
    try:
        config = build_training_config(request)
        trainer = get_trainer(config)
        trainer.train()
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")

        