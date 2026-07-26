"""ChatATP Studio Python SDK."""

from .client import ChatATPClient
from .errors import (
    ChatATPError,
    AuthenticationError,
    PermissionError,
    ValidationError,
    RateLimitError,
    NotFoundError,
    ServerError,
    NetworkError,
    TimeoutError,
)
from .models import (
    Agent,
    AgentCapabilities,
    Conversation,
    ConversationSummary,
    Message,
    SendMessageResponse,
    Usage,
    StreamEvent,
    Page,
)

__version__ = "0.1.1"
__all__ = [
    "ChatATPClient",
    # Errors
    "ChatATPError",
    "AuthenticationError",
    "PermissionError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
    "ServerError",
    "NetworkError",
    "TimeoutError",
    # Models
    "Agent",
    "AgentCapabilities",
    "Conversation",
    "ConversationSummary",
    "Message",
    "SendMessageResponse",
    "Usage",
    "StreamEvent",
    "Page",
]
