from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.infrastructure.database.sqlite.checkpointer import CheckpointerProvider
from app.nexus.executor.graph_executor import GraphExecutor


@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpointer_provider: CheckpointerProvider = CheckpointerProvider()
    checkpointer: BaseCheckpointSaver = await checkpointer_provider.build()

    app.state.graph_executor = GraphExecutor(checkpointer=checkpointer)

    yield

    await checkpointer_provider.close()
