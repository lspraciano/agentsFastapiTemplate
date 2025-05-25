import logging
from typing import Any

from app.infrastructure.logger.langgraph.configure_langgraph_logger import configure_langgraph_logger

langgraph_logger: logging.Logger = configure_langgraph_logger()


def langgraph_log_event(
        event: Any
) -> None:
    event_type: str = event.get("event", "Unknown")
    event_name: str = event.get("name", "Unknown")
    event_data = event.get("data", {})
    event_metadata = event.get("metadata", {})

    log_message: dict = {
        "event_type": event_type,
        "event_name": event_name,
        # "Metadados" : f"{event_metadata}, "
        # "Dados": f"{event_data}"
    }

    if "error" in event_type.lower():
        langgraph_logger.error(log_message)
    elif "debug" in event_type.lower():
        langgraph_logger.debug(log_message)
    else:
        langgraph_logger.info(log_message)
