import logging

from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler

from configuration.configs import settings

logger: logging.Logger = logging.getLogger(name=__name__)


class LangfuseProvider:
    def __init__(self):
        self._client: Langfuse | None = None

    def init(self) -> Langfuse:
        if self._client is not None:
            return self._client

        Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
            environment=settings.current_env,
        )

        client: Langfuse = get_client()

        self._client = client

        logger.info(
            msg="Langfuse inicializado.",
            extra={
                "host": settings.LANGFUSE_HOST,
                "environment": settings.current_env,
            },
        )

        return client

    @property
    def client(self) -> Langfuse:
        return self.init()

    @staticmethod
    def get_callback_handler() -> CallbackHandler:
        return CallbackHandler()

    def flush(self) -> None:
        self.client.flush()
