import json
from typing import AsyncIterable

from app.core.helpers.logger.langgraph.langgraph_logger import langgraph_log_event
from app.core.machine_learning.llm.graphs.main_graph import graph
from app.core.machine_learning.llm.nodes.handlers.translate_langgraph_node_event import translate_langgraph_node_event
from app.core.machine_learning.llm.states.handlers.state_handler import get_state_from_mongo


async def get_llm_response_stream(
        user_message: str,
        conversation_uuid: str,
) -> AsyncIterable:
    nodes_names: set[str] = set()
    state: dict = await get_state_from_mongo(
        conversation_uuid=conversation_uuid
    )

    async for event in graph.astream_events(
            input={
                **state,
                "current_user_message": user_message,
                "conversation_uuid": conversation_uuid,
            },
            config={
                "recursion_limit": 100,
                "configurable": {
                    "thread_id": conversation_uuid
                }
            },
            version="v2"
    ):
        metadata: dict = event.get("metadata", {})
        langgraph_node: str | dict = metadata.get("langgraph_node", {})

        if langgraph_node:
            current_node_name: str = metadata.get("langgraph_node")

            if langgraph_node not in nodes_names:
                langgraph_log_event(event)
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
                "conversation_uuid": conversation_uuid
            }

            json_dump_langgraph_output: str = json.dumps(
                obj=langgraph_output_dict,
                ensure_ascii=False
            )

            yield f"event:llm_event\ndata:{json_dump_langgraph_output}\n\n"
