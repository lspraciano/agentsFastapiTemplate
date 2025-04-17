from pydantic import BaseModel, Field


class BasicChainSchema(BaseModel):
    message: str | None = Field(
        description="""
        Este campo é destinado para enviar mensagens para o usuário
        """
    )
