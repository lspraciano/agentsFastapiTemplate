from pydantic import BaseModel, Field


class AgentCalculatorSchema(BaseModel):
    agent_calculator_response: str = Field(
        description="Resposta final ao usuário, em linguagem natural, com o resultado do cálculo."
    )
