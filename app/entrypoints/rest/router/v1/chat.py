from fastapi import APIRouter, status

from app.entrypoints.rest.dependencies.graph_executor_dependence import GraphExecutorDependence
from app.entrypoints.rest.schemas.chat_schemas import (
    ChatRequestSchema,
    ChatResponseSchema,
)
from app.nexus.contracts.nexus_input import NexusInput
from app.nexus.contracts.nexus_output import NexusOutput

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
    message: ChatRequestSchema,
    executor: GraphExecutorDependence,
) -> ChatResponseSchema:
    nexus_input: NexusInput = NexusInput(
        user_message=message.user_message,
        conversation_id=message.conversation_id,
    )

    nexus_output: NexusOutput = await executor.run(nexus_input=nexus_input)

    return ChatResponseSchema(
        conversation_id=nexus_output.conversation_id,
        response=nexus_output.response,
    )
