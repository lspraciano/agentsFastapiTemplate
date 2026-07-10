import logging
from contextlib import AsyncExitStack

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from configuration.configs import settings

logger: logging.Logger = logging.getLogger(name=__name__)


class CheckpointerProvider:
    def __init__(self):
        self._stack: AsyncExitStack | None = None

    async def build(self) -> BaseCheckpointSaver:
        try:
            stack: AsyncExitStack = AsyncExitStack()

            checkpointer: AsyncSqliteSaver = await stack.enter_async_context(
                cm=AsyncSqliteSaver.from_conn_string(conn_string=settings.SQLITE_PATH)
            )

            await checkpointer.setup()

            self._stack = stack
            logger.info(
                msg="Checkpointer SQLite inicializado.",
                extra={"path": settings.SQLITE_PATH},
            )
            return checkpointer

        except Exception as error:
            logger.warning(
                msg="SQLite indisponível, usando checkpointer em memória.",
                extra={"error": str(error)},
            )
            return InMemorySaver()

    async def close(self) -> None:
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
