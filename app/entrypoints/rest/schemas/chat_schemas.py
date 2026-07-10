from pydantic import BaseModel


class ChatRequestSchema(BaseModel):
    user_message: str
    conversation_id: str


class ChatResponseSchema(BaseModel):
    conversation_id: str
    response: str
