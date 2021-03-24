import logging
import logging.config


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
            "filename": "mediator_ansible_assistant.log",
            "maxBytes": 1073741824,  # 1 GiB
            "backupCount": 3,
            "delay": True,
        }
    },
    "loggers": {
        __name__: {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["default"],
        }
    },
}


def init_logger():
    logging.config.dictConfig(_DEFAULT_LOGGER_CONFIG)
