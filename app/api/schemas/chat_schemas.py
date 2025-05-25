import uuid

from pydantic import BaseModel, model_validator


class BasicMessageSchema(BaseModel):
    user_message: str
    conversation_id: str

    @model_validator(mode="before")
    def generate_id_if_missing(cls, values):
        if "conversation_id" not in values or values["conversation_id"] is None:
            values["conversation_id"]: str = str(uuid.uuid4())
        return values


chat_stream_responses_schema: dict = {
    200: {
        "description": "stream responses in text/event-stream format.",
        "content": {
            "text/event-stream": {
                "examples": {
                    "langgraph_output": {
                        "summary": "message with langgraph_output",
                        "description": "stream message containing the langgraph_output field.",
                        "value": """{"langgraph_output": "value"}\n\n"""
                    },
                    "event_output": {
                        "summary": "message with event",
                        "description": "stream message containing the event field.",
                        "value": """{"event": "value"}\n\n"""
                    }
                }
            }
        },
    },
}
