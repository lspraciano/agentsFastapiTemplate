import json


def translate_langgraph_node_event(
        event_name: str
) -> str:
    translate_dict: dict = {
        "__start__": "Iniciando",
        "memory_checker_node": "iniciando",
        "memory_checker_end_node": "memória não integrada ainda",
        "decide_query_type_node": "decidindo metodologia",
        "decide_query_type_end_node": "decisão não prevista",
        "similarity_retriever_node": "buscando documentos similares",
        "similarity_prepare_documents_node": "preparando documentos similares",
        "similarity_response_node": "gerando resposta",
        "deterministic_generate_query_node": "preparando a busca de documentos",
        "deterministic_execute_query_node": "buscando documentos por keywords",
        "deterministic_prepare_documents_node": "preparando documentos",
        "deterministic_response_node": "gerando resposta",
    }

    output_dict: dict = {
        "langgraph_event": translate_dict.get(event_name, event_name),
    }

    return json.dumps(
        obj=output_dict,
        ensure_ascii=False
    )
