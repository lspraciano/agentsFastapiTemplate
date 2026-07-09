from dataclasses import dataclass


@dataclass
class NexusInput:
    user_message: str
    conversation_id: str
