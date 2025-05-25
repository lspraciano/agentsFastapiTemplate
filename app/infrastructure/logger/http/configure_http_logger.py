import logging

from app.infrastructure.logger.configure_logger import configure_logger


def configure_http_logger() -> logging.Logger:
    return configure_logger(
        log_name="http_logger",
        filename="http_events.log"
    )
