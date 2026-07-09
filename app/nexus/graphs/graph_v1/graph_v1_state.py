from typing import Annotated, TypedDict

from langchain_core.messages.utils import AnyMessage
from langgraph.graph.message import add_messages


class GraphV1State(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    conversation_id: str
    graph_response: str
