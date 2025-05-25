from app.core.graph_engine.structural.states.state import GraphState


async def guardrails_end_node(
        state: GraphState,
) -> dict:
    return {
        "graph_response": (
            "Sua mensagem não pôde ser processada porque contém "
            "conteúdo que viola as diretrizes da plataforma. "
            "Por favor, mantenha um tom respeitoso e evite linguagem "
            "ofensiva, perigosa ou inapropriada. Se precisar de ajuda, "
            "estamos aqui para apoiar da melhor forma possível. "
        )
    }
