from fastapi import APIRouter, Request, status

from app.entrypoints.rest.schemas.chat_schemas import (
    ChatRequestSchema,
    ChatResponseSchema,
)
from app.nexus.contracts.nexus_input import NexusInput
from app.nexus.contracts.nexus_output import NexusOutput
from app.nexus.executor.graph_executor import GraphExecutor

router: APIRouter = APIRouter(
    tags=["Chat"],
    prefix="/chat",
)


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponseSchema,
)
async def chat_(
    request: Request,
    message: ChatRequestSchema,
) -> ChatResponseSchema:
    executor: GraphExecutor = request.app.state.graph_executor

    nexus_input: NexusInput = NexusInput(
        user_message=message.user_message,
        conversation_id=message.conversation_id,
    )

    nexus_output: NexusOutput = await executor.run(nexus_input=nexus_input)

    return ChatResponseSchema(
        conversation_id=nexus_output.conversation_id,
        response=nexus_output.response,
    )
