from typing import Literal

from app.core.graph_engine.structural.states.state import GraphState


async def supervisor_conditionals(
        state: GraphState,
) -> Literal[
    "graph_1_node",
    "graph_2_node",
    "supervisor_end_node",
]:
    supervisor__destination_node: str = state.get("supervisor__destination_node", "")

    if supervisor__destination_node == "graph_1_node":
        return "graph_1_node"
    elif supervisor__destination_node == "graph_2_node":
        return "graph_2_node"
    else:
        return "supervisor_end_node"
