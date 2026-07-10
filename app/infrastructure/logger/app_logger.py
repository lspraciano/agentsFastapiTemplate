import logging.config

from app.infrastructure.logger.json_formatter import JsonFormatter
from configuration.configs import settings


class AppLogger:
    def __init__(self):
        self._config: dict = self._build_config()

    def configure(self) -> None:
        logging.config.dictConfig(config=self._config)

    @staticmethod
    def _build_config() -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                },
            },
            "root": {
                "handlers": ["default"],
                "level": settings.LOG_LEVEL,
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default"],
                    "level": settings.LOG_LEVEL,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": settings.LOG_LEVEL,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": settings.LOG_LEVEL,
                    "propagate": False,
                },
            },
        }
