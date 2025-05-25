from langchain_core.messages import message_to_dict
from langchain_core.messages import messages_from_dict
from langchain_core.messages.base import BaseMessage
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.core.graph_engine.structural.states.state import GraphState
from app.infrastructure.database.mongo.mongo_connection import async_mongodb_client
from configuration.configs import settings

mp_database: AsyncIOMotorDatabase = async_mongodb_client[settings.MONGO_DATABASE]
collection_state: AsyncIOMotorCollection = mp_database[settings.MONGO_COLLECTION_STATE]


def serialize_state(
        state: dict
) -> dict:
    to_serialized: dict = state.copy()

    if "messages" in to_serialized:
        serialized_messages = []

        for message in to_serialized["messages"]:
            if isinstance(message, BaseMessage):
                serialized_messages.append(message_to_dict(message=message))
            else:
                serialized_messages.append(message)

        to_serialized["messages"] = serialized_messages

    return to_serialized


def deserialize_state(
        state: dict
) -> dict:
    deserialized: dict = state.copy()

    if "messages" in deserialized:
        deserialized["messages"] = messages_from_dict(messages=deserialized["messages"])

    return deserialized


async def get_state_from_mongo(
        conversation_id: str,
) -> dict:
    current_state: dict | None = await collection_state.find_one(
        filter={
            "conversation_id": conversation_id
        },
        projection={
            "_id": 0
        }
    )

    if current_state:
        return deserialize_state(
            state=current_state
        )
    return {}


async def save_state_to_mongo(
        state: dict
) -> None:
    conversation_id: str | None = state.get("conversation_id")

    if not conversation_id:
        return

    await collection_state.update_one(
        filter={
            "conversation_id": conversation_id
        },
        update={
            "$set": serialize_state(
                state=state
            )
        },
        upsert=True
    )


async def make_clear_dict(
        state: GraphState
) -> dict:
    fields_to_preserve: set = {
        "messages",
        "conversation_id",
        "graph_response",
        "current_user_message",
    }

    return {
        field: ""
        for field in state
        if field not in fields_to_preserve
    }
