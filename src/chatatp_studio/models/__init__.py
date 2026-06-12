"""Typed model classes representing ChatATP API resources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Iterator, Literal, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class AgentCapabilities:
    persistent_conversations: bool
    streaming: bool
    tool_activity: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "AgentCapabilities":
        return cls(
            persistent_conversations=d["persistent_conversations"],
            streaming=d["streaming"],
            tool_activity=d["tool_activity"],
        )


@dataclass(frozen=True)
class Agent:
    id: int
    name: str
    description: str
    status: str
    avatar_url: str
    capabilities: AgentCapabilities
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Agent":
        return cls(
            id=d["id"],
            name=d["name"],
            description=d["description"],
            status=d["status"],
            avatar_url=d.get("avatar_url", ""),
            capabilities=AgentCapabilities.from_dict(d["capabilities"]),
            created_at=d["created_at"],
            updated_at=d["updated_at"],
        )


@dataclass(frozen=True)
class ConversationSummary:
    id: int
    external_user_id: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ConversationSummary":
        return cls(id=d["id"], external_user_id=d["external_user_id"])


@dataclass(frozen=True)
class Conversation:
    id: int
    agent: Agent
    external_user_id: str
    user_display_name: str | None
    metadata: dict[str, Any]
    message_count: int
    last_message_at: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Conversation":
        return cls(
            id=d["id"],
            agent=Agent.from_dict(d["agent"]),
            external_user_id=d["external_user_id"],
            user_display_name=d.get("user_display_name"),
            metadata=d.get("metadata", {}),
            message_count=d.get("message_count", 0),
            last_message_at=d.get("last_message_at"),
            created_at=d["created_at"],
            updated_at=d["updated_at"],
        )


@dataclass(frozen=True)
class Message:
    id: int
    sender: Literal["user", "agent"]
    content: str
    tool_calls: list[Any]
    metadata: dict[str, Any]
    timestamp: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Message":
        return cls(
            id=d["id"],
            sender=d["sender"],
            content=d["content"],
            tool_calls=d.get("tool_calls", []),
            metadata=d.get("metadata", {}),
            timestamp=d["timestamp"],
        )


@dataclass(frozen=True)
class SendMessageResponse:
    conversation: ConversationSummary
    user_message: Message
    agent_message: Message

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SendMessageResponse":
        return cls(
            conversation=ConversationSummary.from_dict(d["conversation"]),
            user_message=Message.from_dict(d["user_message"]),
            agent_message=Message.from_dict(d["agent_message"]),
        )


@dataclass(frozen=True)
class Usage:
    total_requests: int
    last_request_at: str | None
    by_endpoint: list[dict[str, Any]]
    by_status: list[dict[str, Any]]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Usage":
        return cls(
            total_requests=d["total_requests"],
            last_request_at=d.get("last_request_at"),
            by_endpoint=d.get("by_endpoint", []),
            by_status=d.get("by_status", []),
        )


@dataclass(frozen=True)
class StreamEvent:
    type: str
    data: Any

    @classmethod
    def from_dict(cls, event_type: str, data: Any) -> "StreamEvent":
        return cls(type=event_type, data=data)


@dataclass
class Page(Generic[T]):
    """Iterable wrapper around a list of API results."""

    data: list[T]

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> T:
        return self.data[index]

    @classmethod
    def from_dict(cls, d: dict[str, Any], item_cls: Any) -> "Page[Any]":
        return cls(data=[item_cls.from_dict(item) for item in d["data"]])
