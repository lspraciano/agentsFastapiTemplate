from typing import Annotated

from langchain_core.messages.utils import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class GraphState(TypedDict):
    messages: Annotated[list[tuple[str, str] | AnyMessage], add_messages]
    conversation_id: str
    current_user_message: str
    graph_response: str

    guardrails__is_blocking: bool | None

    supervisor__message: str | None
    supervisor__destination_node: str | None
