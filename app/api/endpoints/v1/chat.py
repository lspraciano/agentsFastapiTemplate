from typing import AsyncIterable


from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from app.core.controllers.chat_controller import get_llm_response_stream
from app.core.schemas.chat_schemas import chat_stream_responses_schema, BasicMessageSchema
from app.core.schemas.generic_responses_schemas import generic_response_400

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
    stream: AsyncIterable = get_llm_response_stream(
        user_message=message.user_message,
        conversation_uuid=str(message.conversation_uuid),
    )

    return StreamingResponse(
        content=stream,
        media_type="text/event-stream",
    )
