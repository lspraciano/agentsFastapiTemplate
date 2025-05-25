import logging
import os
import sys

from configuration.configs import root


def configure_logger(
        log_name: str,
        filename: str
) -> logging.Logger:
    logs_path: str = os.path.join(
        root, "logs"
    )

    os.makedirs(
        logs_path, exist_ok=True
    )

    log_file_path: str = os.path.join(
        logs_path,
        filename
    )

    logger: logging.Logger = logging.getLogger(
        name=log_name
    )

    logger.setLevel(
        level=logging.INFO
    )

    if not logger.handlers:
        console_handler: logging.StreamHandler = logging.StreamHandler(
            stream=sys.stdout
        )

        file_handler: logging.FileHandler = logging.FileHandler(
            filename=log_file_path,
            mode="a",
            encoding="utf-8"
        )

        formatter: logging.Formatter = logging.Formatter(
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
