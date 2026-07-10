import logging

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from app.nexus.contracts.nexus_input import NexusInput
from app.nexus.contracts.nexus_output import NexusOutput
from app.nexus.graphs.graph_v1.graph_v1 import GraphV1

logger: logging.Logger = logging.getLogger(name=__name__)


class GraphResponseMissingError(Exception):
    pass


class GraphExecutor:
    def __init__(
        self,
        checkpointer: BaseCheckpointSaver | None = None,
        callbacks: list[BaseCallbackHandler] | None = None,
    ):
        self._graph: CompiledStateGraph = GraphV1().compile(checkpointer=checkpointer)
        self._callbacks: list[BaseCallbackHandler] = callbacks or []

    async def run(
        self,
        nexus_input: NexusInput,
    ) -> NexusOutput:
        conversation_id: str = nexus_input.conversation_id
        log_context: dict = {"conversation_id": conversation_id}

        logger.info(
            msg="Processando mensagem.",
            extra=log_context,
        )

        config: RunnableConfig = {
            "configurable": {
                "thread_id": conversation_id,
            },
            "metadata": {
                "langfuse_session_id": conversation_id,
            },
            "callbacks": self._callbacks,
        }

        try:
            result: dict = await self._graph.ainvoke(
                input={
                    "messages": [HumanMessage(content=nexus_input.user_message)],
                    "conversation_id": conversation_id,
                },
                config=config,
            )

        except Exception:
            logger.error(
                msg="Falha ao executar o agente.",
                extra=log_context,
                exc_info=True,
            )
            raise

        response: str = result.get("response") or ""

        if not response:
            logger.error(
                msg="Grafo terminou sem 'response'.",
                extra=log_context,
            )

            raise GraphResponseMissingError(
                f"Grafo não produziu 'response' para a conversa {conversation_id}."
            )

        logger.info(
            msg="Resposta gerada.",
            extra=log_context,
        )

        return NexusOutput(
            conversation_id=conversation_id,
            response=response,
        )
