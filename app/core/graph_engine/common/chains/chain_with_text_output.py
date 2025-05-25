from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.tools import BaseTool
from langchain_core.messages.utils import AnyMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.graph_engine.common.models.get_llm_model import get_llm_model


async def chain_with_text_output(
        current_user_message: str,
        messages: list[tuple[str, str] | AnyMessage],
        system_prompt: str,
        instruction_prompt: str,
        llm_model_name: str | None = None,
        tools: list[BaseTool] | None = None,
) -> str | AIMessage:
    parser: StrOutputParser = StrOutputParser()
    prompt: ChatPromptTemplate = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(
                template=system_prompt,
            ),
            MessagesPlaceholder(
                variable_name="messages"
            ),
            HumanMessagePromptTemplate.from_template(
                template=instruction_prompt,
                input_variables=[
                    "current_user_message",
                    "format_instructions",
                ]
            )
        ]
    )

    llm: ChatGoogleGenerativeAI = get_llm_model(
        model_name=llm_model_name
    ) if llm_model_name else get_llm_model()

    if tools:
        chain: Runnable = prompt | llm.bind_tools(tools=tools)
    else:
        chain: Runnable = prompt | llm

    raw_response: AIMessage = chain.invoke(
        input={
            "current_user_message": current_user_message,
            "messages": messages
        }
    )

    if hasattr(
            raw_response,
            "tool_calls"
    ) and raw_response.tool_calls:
        return raw_response

    return parser.invoke(
        input=raw_response
    )
