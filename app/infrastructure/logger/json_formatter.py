import json
import logging
from datetime import datetime, timezone

_RESERVED_ATTRS: frozenset[str] = frozenset(
    {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "taskName",
        "message",
        "asctime",
    }
)


class JsonFormatter(logging.Formatter):
    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload: dict = {
            "timestamp": datetime.fromtimestamp(
                timestamp=record.created,
                tz=timezone.utc,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extras: dict = {}
        for key, value in record.__dict__.items():
            if key not in _RESERVED_ATTRS:
                extras[key] = value

        if extras:
            payload["extra"] = extras

        if record.exc_info:
            payload["exception"] = self.formatException(ei=record.exc_info)

        return json.dumps(
            obj=payload,
            ensure_ascii=False,
            default=str,
        )
