from langchain_core.messages.utils import AnyMessage

from app.core.graph_engine.common.chains.chain_with_structured_output import chain_with_structured_output
from app.core.graph_engine.structural.output_schemas.guardrails_schemas import GuardrailsSchema
from app.core.graph_engine.structural.prompts.guardrails_prompt import (
    GUARDRAILS_SYSTEM_PROMPT,
    GUARDRAILS_INSTRUCTION_PROMPT
)


async def guardrails_chain(
        current_user_message: str,
        messages: list[tuple[str, str] | AnyMessage],
        llm_model_name: str | None = None,
) -> dict:
    return await chain_with_structured_output(
        current_user_message=current_user_message,
        messages=messages,
        llm_model_name=llm_model_name,
        output_schema=GuardrailsSchema,
        system_prompt=GUARDRAILS_SYSTEM_PROMPT,
        instruction_prompt=GUARDRAILS_INSTRUCTION_PROMPT,
    )
