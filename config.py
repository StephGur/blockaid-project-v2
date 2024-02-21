import logging
import os

from flask import Flask


class BaseConfig:
    INFURA_BASE_URL = 'https://mainnet.infura.io/v3'
    INFURA_KEY = os.getenv('INFURA_KEY') or "c48ff3d7542b4031bec16aeb3ce79006"
    INFURA_URL = f'{INFURA_BASE_URL}/{INFURA_KEY}'
    TRANSFER_EVENT_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    LOG_FORMAT = '%()'

    @staticmethod
    def setup_console_logger(app: Flask):
        formatter = logging.Formatter(app.config['LOG_FORMAT'])
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])


class LocalConfig(BaseConfig):
    INFURA_BASE_URL = 'https://mainnet.infura.io/v3'
    INFURA_KEY = os.getenv('INFURA_KEY') or "c48ff3d7542b4031bec16aeb3ce79006"
    INFURA_URL = f'{INFURA_BASE_URL}/{INFURA_KEY}'
    TRANSFER_EVENT_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def get_configuration_by_name(environment: str = 'DEFAULT') -> BaseConfig:
    return {
        'LOCAL': LocalConfig,
        'DEFAULT': LocalConfig
    }[environment]


def get_configuration() -> type(BaseConfig):
    environment: str = os.getenv('FLASK', 'DEFAULT')
    return get_configuration_by_name(environment)


BLOCKAID_CONFIG = get_configuration()
