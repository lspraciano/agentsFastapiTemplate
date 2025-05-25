from typing import Literal

from app.core.graph_engine.structural.states.state import GraphState


async def guardrails_conditionals(
        state: GraphState,
) -> Literal[
    "guardrails_end_node",
    "supervisor_node",
]:
    guardrails__is_blocking: bool | None = state.get("guardrails__is_blocking", "")

    if guardrails__is_blocking:
        return "guardrails_end_node"

    return "supervisor_node"
