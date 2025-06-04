from trainers.ppo_trainer import PPOTrainer
from trainers.grpo_trainer import GRPOTrainer

def get_trainer(config):
    algo = config["training"]["algorithm"]
    if algo == "ppo":
        return PPOTrainer(config)
    elif algo == "gpro":
        return GRPOTrainer(config)
    else:
        raise ValueError(f"Unknown algorithm: {algo}")

