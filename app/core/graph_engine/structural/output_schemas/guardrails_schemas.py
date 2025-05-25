from pydantic import BaseModel, Field


class GuardrailsSchema(BaseModel):
    guardrails__is_blocking: bool | None = Field(
        description="""
        Indica se a mensagem do usuário deve ser bloqueada com base em 
        violação de políticas de segurança, conduta ou conteúdo.
        - **True**: A mensagem contém linguagem tóxica, conteúdo perigoso, ofensivo, 
        ilegal, sexualmente explícito, discriminatório ou qualquer outro material 
        que represente risco à integridade do usuário, da plataforma ou de terceiros.
        - **False**: A mensagem está dentro dos padrões aceitáveis e não apresenta 
        riscos de segurança.
        - **None**: Não foi possível determinar com confiança o status da mensagem 
        (caso ambíguo ou indefinido).
        """
    )
