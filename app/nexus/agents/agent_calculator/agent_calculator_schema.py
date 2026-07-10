from pydantic import BaseModel, Field


class AgentCalculatorSchema(BaseModel):
    response: str = Field(
        description="Resposta final ao usuário, em linguagem natural, com o resultado do cálculo."
    )
