from langchain_core.messages import AnyMessage

from app.core.graph_engine.structural.chains.guardrails_chain import guardrails_chain
from app.core.graph_engine.structural.states.state import GraphState


async def guardrails_node(
        state: GraphState,
) -> dict:
    current_user_message: str = state.get("current_user_message", "")
    messages: list[tuple[str, str] | AnyMessage] = state.get("messages", [])

    guardrails_chain_result: dict = await guardrails_chain(
        current_user_message=current_user_message,
        messages=messages
    )

    return {
        **guardrails_chain_result,
    }
