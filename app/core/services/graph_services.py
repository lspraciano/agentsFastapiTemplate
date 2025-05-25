import json
from typing import AsyncIterable

from app.core.graph_engine.common.handlers.translate_langgraph_node_event import translate_langgraph_node_event
from app.core.graph_engine.main_graph import main_graph
from app.core.services.state_services import get_state_from_mongo_service
from app.infrastructure.logger.langgraph.langgraph_logger import langgraph_log_event


async def stream_langgraph_response_service(
        user_message: str,
        conversation_id: str
) -> AsyncIterable:
    nodes_names: set[str] = set()

    state: dict = await get_state_from_mongo_service(
        conversation_id=conversation_id
    )

    async for event in main_graph.astream_events(
            input={
                **state,
                "current_user_message": user_message,
                "conversation_id": conversation_id,
            },
            config={
                "recursion_limit": 100,
                "configurable": {
                    "thread_id": conversation_id
                }
            },
            version="v2"
    ):
        metadata: dict = event.get("metadata", {})
        langgraph_node: str | dict = metadata.get("langgraph_node", {})

        if langgraph_node:
            current_node_name: str = metadata.get("langgraph_node")

            if langgraph_node not in nodes_names:
                langgraph_log_event(event=event)
                langgraph_node_name: str = metadata.get("langgraph_node")
                translated_event: str = translate_langgraph_node_event(
                    event_name=langgraph_node_name
                )

                yield f"event:llm_event\ndata:{translated_event}\n\n"

            nodes_names.add(current_node_name)

        event_type: str = event.get("event")
        event_name: str = event.get("name")
        is_end_of_chain: bool = event_type == "on_chain_end"
        is_langgraph_event: bool = event_name == "LangGraph"

        if is_end_of_chain and is_langgraph_event:
            current_output: dict | list[dict] = event["data"]["output"]

            langgraph_output_dict: dict = {
                "langgraph_output": current_output["graph_response"],
                "conversation_id": conversation_id
            }

            json_dump_langgraph_output: str = json.dumps(
                obj=langgraph_output_dict,
                ensure_ascii=False
            )

            yield f"event:llm_event\ndata:{json_dump_langgraph_output}\n\n"
