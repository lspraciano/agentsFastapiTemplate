from langchain_core.messages.utils import AnyMessage

from app.core.graph_engine.common.chains.chain_with_structured_output import chain_with_structured_output
from app.core.graph_engine.structural.output_schemas.supervisor_schemas import SupervisorSchema
from app.core.graph_engine.structural.prompts.supervisor_prompt import (
    SUPERVISOR_SYSTEM_PROMPT,
    SUPERVISOR_INSTRUCTION_PROMPT
)


async def supervisor_chain(
        current_user_message: str,
        messages: list[tuple[str, str] | AnyMessage],
        llm_model_name: str | None = None,
) -> dict:
    return await chain_with_structured_output(
        current_user_message=current_user_message,
        messages=messages,
        llm_model_name=llm_model_name,
        output_schema=SupervisorSchema,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        instruction_prompt=SUPERVISOR_INSTRUCTION_PROMPT,
    )
