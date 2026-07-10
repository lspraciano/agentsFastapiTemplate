from abc import ABC, abstractmethod
from typing import Any

from langchain.agents import AgentState, create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from pydantic import BaseModel

from app.nexus.middlewares.structured_response_retry_middleware import (
    StructuredResponseRetryMiddleware,
)
from app.nexus.middlewares.tool_loop_guard_middleware import ToolLoopGuardMiddleware


class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        schema: type[BaseModel],
        system_prompt: str,
        tools: list | None = None,
        extra_middleware: list | None = None,
        state_schema: type[AgentState] | None = None,
    ):
        self.name: str = name
        self.schema: type[BaseModel] = schema
        self.system_prompt: str = system_prompt
        self.tools: list = tools or []
        self.state_schema: type[AgentState] | None = state_schema
        self.middleware: list = [
            ToolLoopGuardMiddleware(),
            StructuredResponseRetryMiddleware(schema=self.schema),
            *(extra_middleware or []),
        ]
        self._llm_model: BaseChatModel = self._create_llm()
        self.agent: CompiledStateGraph = create_agent(
            name=self.name,
            model=self._llm_model,
            response_format=self.schema,
            tools=self.tools,
            middleware=self.middleware,
            state_schema=self.state_schema,
        )

    async def __call__(
        self,
        state: dict,
    ) -> Command:
        messages: list[BaseMessage] = self._get_messages(state=state)

        system_prompt: str = self._build_system_prompt(state=state)

        agent_messages: list[BaseMessage] = [
            SystemMessage(content=system_prompt),
            *messages,
        ]

        invoke_input: dict = self._build_invoke_input(
            state=state,
            agent_messages=agent_messages,
        )

        agent_result: dict = await self.agent.ainvoke(input=invoke_input)

        structured: Any = agent_result["structured_response"]

        return self._build_command(
            structured=structured,
            state=state,
        )

    @staticmethod
    def _get_messages(
        state: dict,
    ) -> list[BaseMessage]:
        messages: list[BaseMessage] = state.get("messages", [])

        return messages

    def _build_system_prompt(
        self,
        state: dict,
    ) -> str:
        return self.system_prompt

    @staticmethod
    def _build_invoke_input(
        state: dict,
        agent_messages: list[BaseMessage],
    ) -> dict:
        return {"messages": agent_messages}

    @abstractmethod
    def _create_llm(self) -> BaseChatModel: ...

    @abstractmethod
    def _build_command(
        self,
        structured: Any,
        state: dict,
    ) -> Command: ...
