from langchain_core.messages import HumanMessage, AIMessage

from app.core.graph_engine.structural.states.state import GraphState


async def update_messages_node(
        state: GraphState
) -> dict:
    current_user_message: str = state.get("current_user_message")
    graph_response: str = state.get("graph_response", "")

    return {
        "messages": [
            HumanMessage(content=current_user_message),
            AIMessage(content=graph_response)
        ]
    }
