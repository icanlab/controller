import logging
import logging.config
import os

import yaml

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_DEFAULT_LOGGER_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)d %(message)s"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "mediator-controller.log",
            "maxBytes": 1073741824,  # 1 GiB
            "backupCount": 3,
            "delay": True,
        }
    },
    "loggers": {
        __name__: {
            "level": "INFO",
            "propagate": False,
            "handlers": ["default"],
        }
    },
}


def init_logger():
    logging.config.dictConfig(_DEFAULT_LOGGER_CONFIG)


def load_app_config(app):
    config_path = os.path.expanduser("~/.mediator/controller.yml")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.info('fail to load configuration "{}", use default configuration'.format(e))
    else:
        if not isinstance(data, dict):
            raise RuntimeError("error config file, require dict")
        for k, v in data.items():
            app.config[k] = v
