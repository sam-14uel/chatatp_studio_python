"""Shared test fixtures and helpers."""

from __future__ import annotations

AGENT_PAYLOAD = {
    "id": 7,
    "name": "Support Agent",
    "description": "Answers product questions.",
    "status": "active",
    "avatar_url": "https://example.com/avatar.png",
    "capabilities": {"persistent_conversations": True, "streaming": True, "tool_activity": True},
    "created_at": "2026-06-12T00:00:00Z",
    "updated_at": "2026-06-12T00:00:00Z",
}

CONVERSATION_PAYLOAD = {
    "id": 91,
    "agent": AGENT_PAYLOAD,
    "external_user_id": "user_12345",
    "user_display_name": "Jane Customer",
    "metadata": {"developer_api": True},
    "message_count": 0,
    "last_message_at": None,
    "created_at": "2026-06-12T00:00:00Z",
    "updated_at": "2026-06-12T00:00:00Z",
}

USER_MESSAGE_PAYLOAD = {
    "id": 501,
    "sender": "user",
    "content": "Do you ship to Lagos?",
    "tool_calls": [],
    "metadata": {},
    "timestamp": "2026-06-12T00:00:00Z",
}

AGENT_MESSAGE_PAYLOAD = {
    "id": 502,
    "sender": "agent",
    "content": "Yes, shipping is available.",
    "tool_calls": [],
    "metadata": {},
    "timestamp": "2026-06-12T00:00:01Z",
}

SEND_RESPONSE_PAYLOAD = {
    "conversation": {"id": 91, "external_user_id": "user_12345"},
    "user_message": USER_MESSAGE_PAYLOAD,
    "agent_message": AGENT_MESSAGE_PAYLOAD,
}

USAGE_PAYLOAD = {
    "total_requests": 248,
    "last_request_at": "2026-06-12T01:30:00Z",
    "by_endpoint": [{"endpoint": "/v1/conversations/91/messages/", "count": 120}],
    "by_status": [{"status_code": 200, "count": 240}],
}
