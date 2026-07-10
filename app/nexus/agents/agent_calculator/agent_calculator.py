from typing import Any

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.types import Command

from app.nexus.agents.agent_calculator.agent_calculator_schema import (
    AgentCalculatorSchema,
)
from app.nexus.agents.agent_calculator.agent_calculator_system_prompt import (
    agent_calculator_system_prompt,
)
from app.nexus.agents.base_agent import BaseAgent
from app.nexus.tools.calculate_tool import calculate_tool
from configuration.configs import settings


class AgentCalculator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="agent_calculator",
            schema=AgentCalculatorSchema,
            system_prompt=agent_calculator_system_prompt,
            tools=[calculate_tool],
        )

    def _create_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0,
            timeout=settings.LLM_SERVICE_TIMEOUT,
            api_key=settings.OPENAI_API_KEY,
        )

    def _build_command(
        self,
        structured: Any,
        state: dict,
    ) -> Command:
        ai_message: AIMessage = AIMessage(
            content=structured.response,
            name=self.agent.name,
        )

        update: dict = {
            **structured.model_dump(exclude_defaults=True),
            "messages": [ai_message],
        }

        return Command(
            goto=END,
            update=update,
        )
