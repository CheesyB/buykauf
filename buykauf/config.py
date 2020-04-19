import os


class Config(object):

    def __init__(self):
        self.config = {}
        self.config['TOKEN'] = os.getenv("TOKEN")
        self.config['CONNECTION'] = os.getenv("CONNECTION")

    def __getitem__(self, item):
        return self.config[item]

    def __len__(self):
        return len(self.config)
