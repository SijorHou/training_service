class BaseTrainer:
    def __init__(self, config):
        self.config = config

    def train(self):
        raise NotImplementedError("train() must be implemented by subclasses")


