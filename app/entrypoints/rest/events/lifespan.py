import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.infrastructure.database.sqlite.checkpointer import CheckpointerProvider
from app.infrastructure.observability.langfuse.langfuse_provider import LangfuseProvider
from app.nexus.executor.graph_executor import GraphExecutor

logger: logging.Logger = logging.getLogger(name=__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    langfuse_provider: LangfuseProvider = LangfuseProvider()
    langfuse_provider.init()
    langfuse_handler: CallbackHandler = langfuse_provider.get_callback_handler()

    checkpointer_provider: CheckpointerProvider = CheckpointerProvider()
    checkpointer: BaseCheckpointSaver = await checkpointer_provider.build()

    app.state.graph_executor = GraphExecutor(
        checkpointer=checkpointer,
        callbacks=[langfuse_handler],
    )
    logger.info(msg="Aplicação iniciada.")

    yield

    logger.info(msg="Encerrando aplicação, liberando recursos.")
    langfuse_provider.flush()
    await checkpointer_provider.close()
