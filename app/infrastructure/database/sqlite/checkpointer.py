from contextlib import AsyncExitStack

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from configuration.configs import settings


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
            return checkpointer

        except Exception:
            return InMemorySaver()

    async def close(self) -> None:
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
