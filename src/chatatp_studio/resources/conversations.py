"""Conversations resource."""

from __future__ import annotations

from typing import Any

from .._requester import Requester
from ..models import Conversation, ConversationSummary, Page


class ConversationsResource:
    def __init__(self, requester: Requester) -> None:
        self._r = requester

    async def create(
        self,
        agent_id: int,
        external_user_id: str,
        *,
        user_display_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Conversation:
        """Create or upsert a conversation."""
        body: dict[str, Any] = {"agent_id": agent_id, "external_user_id": external_user_id}
        if user_display_name is not None:
            body["user_display_name"] = user_display_name
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._r.request("POST", "/v1/conversations/", body=body)
        return Conversation.from_dict(data)

    async def retrieve(self, conversation_id: int) -> Conversation:
        """Retrieve a conversation by ID."""
        data = await self._r.request("GET", f"/v1/conversations/{conversation_id}/")
        return Conversation.from_dict(data)

    async def list(
        self,
        *,
        agent_id: int | None = None,
        external_user_id: str | None = None,
    ) -> Page[ConversationSummary]:
        """List conversations, optionally filtered."""
        data = await self._r.request(
            "GET",
            "/v1/conversations/",
            params={"agent_id": agent_id, "external_user_id": external_user_id},
        )
        return Page.from_dict(data, ConversationSummary)

    async def delete(self, conversation_id: int) -> None:
        """Permanently delete a conversation."""
        await self._r.request("DELETE", f"/v1/conversations/{conversation_id}/")
