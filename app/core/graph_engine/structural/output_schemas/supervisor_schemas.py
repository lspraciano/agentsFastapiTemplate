from pydantic import BaseModel, Field


class SupervisorSchema(BaseModel):
    supervisor__message: str = Field(
        description="""
        Este campo é destinado para enviar mensagens para o usuário
        """
    )
    supervisor__destination_node: str = Field(
        description="""
        Este campo é destinado a receber o nome do fluxo identificado pelo supervisor
        """
    )
