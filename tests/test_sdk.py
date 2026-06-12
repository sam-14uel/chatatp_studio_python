"""Tests for the ChatATP Studio Python SDK."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chatatp_studio import (
    AuthenticationError,
    ChatATPClient,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from chatatp_studio.models import Agent, Conversation, Message, SendMessageResponse, Usage

from .fixtures import (
    AGENT_PAYLOAD,
    AGENT_MESSAGE_PAYLOAD,
    CONVERSATION_PAYLOAD,
    SEND_RESPONSE_PAYLOAD,
    USAGE_PAYLOAD,
    USER_MESSAGE_PAYLOAD,
)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


def _make_response(status: int, body: object) -> MagicMock:
    """Create a mock httpx.Response."""
    resp = MagicMock()
    resp.status_code = status
    resp.is_success = 200 <= status < 300
    resp.json.return_value = body
    resp.headers = {}
    return resp


def _patch_request(client: ChatATPClient, status: int, body: object) -> AsyncMock:
    mock = AsyncMock(return_value=_make_response(status, body))
    client._requester._client.request = mock
    return mock


# ──────────────────────────────────────────────
# Client construction
# ──────────────────────────────────────────────


def test_client_requires_api_key():
    with pytest.raises(ValueError, match="api_key is required"):
        ChatATPClient("")


# ──────────────────────────────────────────────
# Agents
# ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_agents_list():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 200, {"data": [AGENT_PAYLOAD]})

    page = await client.agents.list()
    assert len(page) == 1
    assert isinstance(page[0], Agent)
    assert page[0].id == 7
    assert page[0].name == "Support Agent"


@pytest.mark.asyncio
async def test_agents_list_iterable():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 200, {"data": [AGENT_PAYLOAD]})

    page = await client.agents.list()
    items = list(page)
    assert len(items) == 1


@pytest.mark.asyncio
async def test_agents_retrieve():
    client = ChatATPClient("chatatp_sk_test")
    mock = _patch_request(client, 200, AGENT_PAYLOAD)

    agent = await client.agents.retrieve(7)
    assert agent.id == 7
    assert agent.capabilities.streaming is True

    call_args = mock.call_args
    assert "/v1/agents/7/" in str(call_args)


# ──────────────────────────────────────────────
# Conversations
# ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_conversations_create():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 200, CONVERSATION_PAYLOAD)

    conv = await client.conversations.create(7, "user_12345")
    assert isinstance(conv, Conversation)
    assert conv.id == 91
    assert conv.agent.id == 7


@pytest.mark.asyncio
async def test_conversations_list():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(
        client, 200, {"data": [{"id": 91, "external_user_id": "user_12345"}]}
    )

    page = await client.conversations.list(agent_id=7)
    assert len(page) == 1
    assert page[0].id == 91


@pytest.mark.asyncio
async def test_conversations_delete():
    client = ChatATPClient("chatatp_sk_test")
    mock = _patch_request(client, 204, None)
    # Override is_success for 204
    mock.return_value.is_success = True
    mock.return_value.status_code = 204

    result = await client.conversations.delete(91)
    assert result is None


# ──────────────────────────────────────────────
# Messages
# ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_messages_list():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(
        client, 200, {"data": [USER_MESSAGE_PAYLOAD, AGENT_MESSAGE_PAYLOAD]}
    )

    page = await client.messages.list(91)
    assert len(page) == 2
    assert isinstance(page[0], Message)
    assert page[0].sender == "user"
    assert page[1].sender == "agent"


@pytest.mark.asyncio
async def test_messages_send():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 200, SEND_RESPONSE_PAYLOAD)

    result = await client.messages.send(91, "Do you ship to Lagos?")
    assert isinstance(result, SendMessageResponse)
    assert result.user_message.content == "Do you ship to Lagos?"
    assert result.agent_message.content == "Yes, shipping is available."


# ──────────────────────────────────────────────
# Usage
# ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_usage_retrieve():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 200, USAGE_PAYLOAD)

    usage = await client.usage.retrieve()
    assert isinstance(usage, Usage)
    assert usage.total_requests == 248


# ──────────────────────────────────────────────
# High-level chat interface
# ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_chat_creates_conversation_then_sends():
    client = ChatATPClient("chatatp_sk_test")
    call_count = 0
    responses = [
        _make_response(200, CONVERSATION_PAYLOAD),
        _make_response(200, SEND_RESPONSE_PAYLOAD),
    ]

    async def side_effect(*args, **kwargs):
        nonlocal call_count
        r = responses[call_count]
        call_count += 1
        return r

    client._requester._client.request = AsyncMock(side_effect=side_effect)

    result = await client.chat(7, "user_12345", "Do you ship to Lagos?")
    assert call_count == 2
    assert result.agent_message.content == "Yes, shipping is available."


# ──────────────────────────────────────────────
# Error handling
# ──────────────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,exc_class",
    [
        (401, AuthenticationError),
        (403, PermissionError),
        (400, ValidationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ServerError),
    ],
)
async def test_error_mapping(status: int, exc_class: type):
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, status, {"detail": "error"})
    # Disable retries for speed
    client._requester._max_retries = 0

    with pytest.raises(exc_class):
        await client.agents.list()


@pytest.mark.asyncio
async def test_error_exposes_status_code_and_payload():
    client = ChatATPClient("chatatp_sk_test")
    _patch_request(client, 404, {"detail": "Agent not found."})
    client._requester._max_retries = 0

    with pytest.raises(NotFoundError) as exc_info:
        await client.agents.retrieve(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.payload == {"detail": "Agent not found."}
