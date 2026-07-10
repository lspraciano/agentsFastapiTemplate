from dataclasses import dataclass


@dataclass
class NexusOutput:
    conversation_id: str
    response: str
