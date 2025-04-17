from langchain.prompts import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages.utils import AnyMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables.base import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.core.machine_learning.llm.llm_models.get_llm_model import get_llm_model
from app.core.machine_learning.llm.prompts.basic_prompt import (
    BASIC_SYSTEM_PROMPT,
    BASIC_INSTRUCTION_PROMPT
)
from app.core.schemas.chain_basic_schemas import BasicChainSchema


async def basic_chain(
        current_user_message: str,
        messages: list[tuple[str, str] | AnyMessage],
        llm_model_name: str | None = None,
) -> dict:
    parser: JsonOutputParser = JsonOutputParser(pydantic_object=BasicChainSchema)
    format_instructions: str = parser.get_format_instructions()
    prompt: ChatPromptTemplate = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(
                template=BASIC_SYSTEM_PROMPT,
            ),
            MessagesPlaceholder(
                variable_name="messages"
            ),
            HumanMessagePromptTemplate.from_template(
                template=BASIC_INSTRUCTION_PROMPT,
                input_variables=[
                    "current_user_message",
                    "format_instructions",
                ]
            )
        ]
    )

    llm: ChatOpenAI | ChatGoogleGenerativeAI = get_llm_model(
        model_name=llm_model_name
    ) if llm_model_name else get_llm_model()

    chain: Runnable = prompt | llm | parser

    return chain.invoke(
        input={
            "current_user_message": current_user_message,
            "messages": messages,
            "format_instructions": format_instructions
        }
    )
