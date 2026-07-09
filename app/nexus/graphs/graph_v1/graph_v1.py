from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.nexus.agents.agent_calculator.agent_calculator import AgentCalculator
from app.nexus.graphs.graph_v1.graph_v1_state import GraphV1State


class GraphV1:
    def __init__(self):
        self._agent_calculator: AgentCalculator = AgentCalculator()

    def compile(
        self,
        checkpointer: BaseCheckpointSaver | None = None,
    ) -> CompiledStateGraph:
        graph: StateGraph = StateGraph(state_schema=GraphV1State)

        graph.add_node(node="agent_calculator", action=self._agent_calculator)

        graph.add_edge(start_key=START, end_key="agent_calculator")

        return graph.compile(checkpointer=checkpointer)
