from langchain_core.messages import AnyMessage

from app.core.graph_engine.graph_2.chains.graph_2_chain import graph_2_chain
from app.core.graph_engine.structural.states.state import GraphState


async def graph_2_node(
        state: GraphState
) -> dict:
    current_user_message: str = state.get("current_user_message", "")
    messages: list[tuple[str, str] | AnyMessage] = state.get("messages", [])

    graph_1_chain_result: str = await graph_2_chain(
        current_user_message=current_user_message,
        messages=messages,
    )

    return {
        "graph_response": graph_1_chain_result,
    }
