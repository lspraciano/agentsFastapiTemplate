from langchain_core.messages import AnyMessage

from app.core.graph_engine.structural.chains.supervisor_chain import supervisor_chain
from app.core.graph_engine.structural.states.state import GraphState


async def supervisor_node(
        state: GraphState
) -> dict:
    current_user_message: str = state.get("current_user_message", "")
    messages: list[tuple[str, str] | AnyMessage] = state.get("messages", [])

    supervisor_chain_result: dict = await supervisor_chain(
        current_user_message=current_user_message,
        messages=messages,
    )

    return {
        **supervisor_chain_result,
        "graph_response": supervisor_chain_result["supervisor__message"]
    }
