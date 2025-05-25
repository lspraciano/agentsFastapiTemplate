from app.infrastructure.repository.state_repository import save_state_to_mongo, get_state_from_mongo


async def save_state_to_mongo_service(
        state: dict
) -> None:
    await save_state_to_mongo(
        state=state
    )


async def get_state_from_mongo_service(
        conversation_id: str,
) -> dict:
    return await get_state_from_mongo(
        conversation_id=conversation_id,
    )
