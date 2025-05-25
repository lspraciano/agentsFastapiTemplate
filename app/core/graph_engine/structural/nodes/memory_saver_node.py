from app.core.graph_engine.structural.states.state import GraphState
from app.core.services.state_services import save_state_to_mongo_service


async def memory_saver_node(
        state: GraphState
) -> dict:
    await save_state_to_mongo_service(
        state=state
    )

    return state
