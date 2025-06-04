from trainers.base import BaseTrainer
from utils.runner import run_script

class PPOTrainer(BaseTrainer):
    def train(self):
        cfg = self.config
        run_script(["python", cfg["data"]["script"], "--collection", cfg["data"]["collection"]])
        run_script([
            "python", "train_ppo.py",
            "--model", cfg["model"],
            "--lr", str(cfg["training"]["arguments"]["lr"]),
            "--steps", str(cfg["training"]["arguments"]["steps"]),
            "--reward", cfg["training"]["reward_fn"]
        ])

        
