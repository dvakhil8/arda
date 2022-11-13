import configparser
import os


class ConfigSupport:
    def __init__(self):
        if os.environ.get('CONFIG_FILE', -1) != -1:
            self.config = self.read_config(os.environ.get('CONFIG_FILE'))

        else:
            raise FileNotFoundError('config file not found. please set CONFIG_FILE env variable')

    def read_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def get_config(self, config_name):
        return self.config[config_name]
