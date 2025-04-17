import logging
import sys


def configure_langgraph_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger(
        name=__name__
    )
    logger.setLevel(
        level=logging.INFO
    )
    console_handler: logging.StreamHandler = logging.StreamHandler(
        stream=sys.stdout
    )
    file_handler: logging.FileHandler = logging.FileHandler(
        filename="langgraph_events.log",
        mode="a",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(
        fmt=formatter
    )

    file_handler.setFormatter(
        fmt=formatter
    )

    logger.addHandler(
        hdlr=console_handler
    )

    logger.addHandler(
        hdlr=file_handler
    )

    return logger
