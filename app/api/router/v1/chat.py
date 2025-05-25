from typing import AsyncIterable

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.api.schemas.chat_schemas import chat_stream_responses_schema, BasicMessageSchema
from app.api.schemas.generic_responses_schemas import generic_response_400
from app.core.services.graph_services import stream_langgraph_response_service

router: APIRouter = APIRouter(
    tags=["Chat"],
    prefix="/chat"
)


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        **chat_stream_responses_schema,
        **generic_response_400
    },
    response_class=StreamingResponse
)
async def chat_(
        message: BasicMessageSchema
):
    stream: AsyncIterable = stream_langgraph_response_service(
        user_message=message.user_message,
        conversation_id=message.conversation_id,
    )

    return StreamingResponse(
        content=stream,
        media_type="text/event-stream",
    )
