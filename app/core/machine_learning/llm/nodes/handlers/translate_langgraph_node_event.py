import json


def translate_langgraph_node_event(
        event_name: str
) -> str:
    translate_dict: dict = {
        "__start__": "Iniciando",
        "basic_node": "nó basico",
    }

    output_dict: dict = {
        "langgraph_event": translate_dict.get(event_name, event_name),
    }

    return json.dumps(
        obj=output_dict,
        ensure_ascii=False
    )
