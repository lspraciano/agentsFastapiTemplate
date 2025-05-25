import logging

from app.infrastructure.logger.configure_logger import configure_logger


def configure_langgraph_logger() -> logging.Logger:
    return configure_logger(
        log_name="langgraph_logger",
        filename="langgraph_events.log"
    )
