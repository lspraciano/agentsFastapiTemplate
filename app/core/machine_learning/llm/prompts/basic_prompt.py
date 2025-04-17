BASIC_SYSTEM_PROMPT: str = """
Você é um assistênte que faz parte de uma código de demonstração de 
funcionamento do langgraph.
"""

BASIC_INSTRUCTION_PROMPT: str = """
[MENSAGEM ATUAL DO USUÁRIO]
{current_user_message}

[INSTRUÇÕES FINAIS]
- Responda obrigatoriamente no seguinte formato JSON:
{format_instructions}
"""