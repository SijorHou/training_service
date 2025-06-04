from trainers.base import BaseTrainer
from utils.runner import run_script

class GRPOTrainer(BaseTrainer):
    def train(self):
        cfg = self.config
        run_script(["python", cfg["data"]["script"], "--collection", cfg["data"]["collection"]])
        run_script([
            "python", "train_gpro.py",
            "--model", cfg["model"],
            "--reward", cfg["training"]["reward_fn"]
        ])

    