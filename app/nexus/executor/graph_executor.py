from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from app.nexus.contracts.nexus_input import NexusInput
from app.nexus.contracts.nexus_output import NexusOutput
from app.nexus.graphs.graph_v1.graph_v1 import GraphV1


class GraphExecutor:
    def __init__(
        self,
        checkpointer: BaseCheckpointSaver | None = None,
    ):
        self._graph: CompiledStateGraph = GraphV1().compile(checkpointer=checkpointer)

    async def run(
            self,
            nexus_input: NexusInput,
    ) -> NexusOutput:
        config: RunnableConfig = {
            "configurable": {
                "thread_id": nexus_input.conversation_id,
            },
        }

        result: dict = await self._graph.ainvoke(
            input={
                "messages": [HumanMessage(content=nexus_input.user_message)],
                "conversation_id": nexus_input.conversation_id,
            },
            config=config,
        )

        return NexusOutput(
            conversation_id=nexus_input.conversation_id,
            response=result.get("graph_response", ""),
        )
