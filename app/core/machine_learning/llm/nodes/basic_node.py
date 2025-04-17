from langchain_core.messages import AnyMessage

from app.core.machine_learning.llm.chains.basic_chain import basic_chain
from app.core.machine_learning.llm.states.state import GraphState


async def basic_node(
        state: GraphState
) -> dict:
    current_user_message: str = state.get("current_user_message")
    messages: list[tuple[str, str] | AnyMessage] = state.get("messages", [])

    basic_chain_result: dict = await basic_chain(
        current_user_message=current_user_message,
        messages=messages
    )

    graph_response: str | None = basic_chain_result["message"]

    return {
        "graph_response": graph_response
    }
