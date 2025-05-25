from langchain_core.messages.utils import AnyMessage

from app.core.graph_engine.common.chains.chain_with_text_output import chain_with_text_output
from app.core.graph_engine.graph_2.prompts.graph_2_prompts import GRAPH_2_SYSTEM_PROMPT, GRAPH_2_INSTRUCTION_PROMPT


async def graph_2_chain(
        current_user_message: str,
        messages: list[tuple[str, str] | AnyMessage],
        llm_model_name: str | None = None,
) -> str:
    return await chain_with_text_output(
        current_user_message=current_user_message,
        messages=messages,
        llm_model_name=llm_model_name,
        system_prompt=GRAPH_2_SYSTEM_PROMPT,
        instruction_prompt=GRAPH_2_INSTRUCTION_PROMPT,
    )
