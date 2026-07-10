class NexusError(Exception):
    code: str = "nexus_error"


class GraphResponseMissingError(NexusError):
    code: str = "graph_response_missing"


class StructuredResponseRetryExceededError(NexusError):
    code: str = "structured_response_retry_exceeded"
