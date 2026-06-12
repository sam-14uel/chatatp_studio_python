"""Messages resource."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from .._requester import Requester
from ..models import Message, Page, SendMessageResponse, StreamEvent


class MessagesResource:
    def __init__(self, requester: Requester) -> None:
        self._r = requester

    async def list(self, conversation_id: int) -> Page[Message]:
        """Retrieve the full message history for a conversation."""
        data = await self._r.request("GET", f"/v1/conversations/{conversation_id}/messages/")
        return Page.from_dict(data, Message)

    async def send(
        self,
        conversation_id: int,
        content: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> SendMessageResponse:
        """Send a message and return both user and agent messages."""
        body: dict[str, Any] = {"content": content}
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._r.request(
            "POST",
            f"/v1/conversations/{conversation_id}/messages/",
            body=body,
        )
        return SendMessageResponse.from_dict(data)

    async def stream(
        self,
        conversation_id: int,
        content: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Stream a message response as an async generator of StreamEvent objects.

        Usage::

            async for event in client.messages.stream(91, "Do you ship to Lagos?"):
                if event.type == "agent.response.completed":
                    print(event.data)
        """
        body: dict[str, Any] = {"content": content}
        if metadata is not None:
            body["metadata"] = metadata

        return self._event_generator(
            self._r.stream(f"/v1/conversations/{conversation_id}/messages/stream/", body)
        )

    async def _event_generator(
        self,
        source: AsyncGenerator[dict[str, Any], None],
    ) -> AsyncGenerator[StreamEvent, None]:
        async for raw in source:
            yield StreamEvent.from_dict(raw["type"], raw["data"])
