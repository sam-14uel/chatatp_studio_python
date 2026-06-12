"""Main ChatATP Studio client."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from ._requester import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, Requester
from .models import SendMessageResponse, StreamEvent
from .resources import AgentsResource, ConversationsResource, MessagesResource, UsageResource


class ChatATPClient:
    """
    Async client for the ChatATP Studio Developer API.

    Usage::

        import asyncio
        from chatatp_studio import ChatATPClient

        async def main():
            client = ChatATPClient(api_key="chatatp_sk_...")
            result = await client.chat(
                agent_id=7,
                external_user_id="user_12345",
                message="Do you ship to Lagos?",
            )
            print(result.agent_message.content)
            await client.aclose()

        asyncio.run(main())

    Or as a context manager::

        async with ChatATPClient(api_key="chatatp_sk_...") as client:
            ...
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        debug: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        self._requester = Requester(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            debug=debug,
        )

        self.agents = AgentsResource(self._requester)
        self.conversations = ConversationsResource(self._requester)
        self.messages = MessagesResource(self._requester)
        self.usage = UsageResource(self._requester)

    # ──────────────────────────────────────────────
    # High-level chat interface
    # ──────────────────────────────────────────────

    async def chat(
        self,
        agent_id: int,
        external_user_id: str,
        message: str,
        *,
        user_display_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> SendMessageResponse:
        """
        Send a message to an agent on behalf of a user.

        The SDK automatically creates or retrieves the underlying conversation,
        so you only need the agent ID, user ID, and message content.

        :param agent_id: The ID of the agent to send the message to.
        :param external_user_id: Your unique identifier for the end user.
        :param message: The message content to send.
        :param user_display_name: Optional human-readable name for the user.
        :param metadata: Optional key-value metadata attached to the conversation.
        :returns: A SendMessageResponse with ``user_message`` and ``agent_message``.
        """
        conversation = await self.conversations.create(
            agent_id,
            external_user_id,
            user_display_name=user_display_name,
            metadata=metadata,
        )
        return await self.messages.send(conversation.id, message)

    async def chat_stream(
        self,
        agent_id: int,
        external_user_id: str,
        message: str,
        *,
        user_display_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Stream a message response from an agent.

        Like :meth:`chat`, conversation lifecycle is handled automatically.

        Usage::

            async for event in client.chat_stream(7, "user_12345", "Hello"):
                if event.type == "agent.response.completed":
                    print(event.data)
        """
        conversation = await self.conversations.create(
            agent_id,
            external_user_id,
            user_display_name=user_display_name,
            metadata=metadata,
        )
        return await self.messages.stream(conversation.id, message)

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self._requester.aclose()

    async def __aenter__(self) -> "ChatATPClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
