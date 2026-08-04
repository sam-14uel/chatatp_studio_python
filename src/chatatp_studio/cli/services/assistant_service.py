"""Assistant / Copilot chat, config, sessions, and analytics service."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .. import endpoints
from ..api_client import APIClient


class AssistantService:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def chat(self, messages: List[Dict[str, str]], session_id: Optional[str] = None) -> Any:
        payload: Dict[str, Any] = {"messages": messages}
        if session_id:
            payload["session_id"] = session_id
        return self.client.post(endpoints.ASSISTANT_CHAT, payload)

    def get_config(self) -> Any:
        return self.client.get(endpoints.ASSISTANT_CONFIG)

    def update_config(self, **fields: Any) -> Any:
        return self.client.patch(endpoints.ASSISTANT_CONFIG, json_body=fields)

    def list_sessions(self) -> Any:
        return self.client.get(endpoints.ASSISTANT_SESSIONS)

    def create_session(self, title: Optional[str] = None) -> Any:
        return self.client.post(endpoints.ASSISTANT_SESSION_CREATE, {"title": title} if title else {})

    def get_session(self, session_id: str) -> Any:
        return self.client.get(endpoints.ASSISTANT_SESSION_DETAIL.format(id=session_id))

    def update_session(self, session_id: str, title: str) -> Any:
        return self.client.patch(endpoints.ASSISTANT_SESSION_DETAIL.format(id=session_id), {"title": title})

    def delete_session(self, session_id: str) -> Any:
        return self.client.delete(endpoints.ASSISTANT_SESSION_DETAIL.format(id=session_id))

    def session_state(self, session_id: str) -> Any:
        return self.client.get(endpoints.ASSISTANT_SESSION_STATE.format(id=session_id))

    def stop_session(self, session_id: str) -> Any:
        return self.client.post(endpoints.ASSISTANT_SESSION_STOP.format(id=session_id))

    def retry_session(self, session_id: str, from_event_id: int) -> Any:
        return self.client.post(
            endpoints.ASSISTANT_SESSION_RETRY.format(id=session_id), {"from_event_id": from_event_id}
        )

    def list_events(self, session_id: str) -> Any:
        return self.client.get(endpoints.ASSISTANT_SESSION_EVENTS.format(id=session_id))

    def edit_event(self, session_id: str, event_id: int, content: str) -> Any:
        return self.client.patch(
            endpoints.ASSISTANT_SESSION_EVENT_DETAIL.format(id=session_id, event_id=event_id), {"content": content}
        )

    def regenerate_event(self, session_id: str, event_id: int, prompt: Optional[str] = None) -> Any:
        payload = {"prompt": prompt} if prompt else {}
        return self.client.post(
            endpoints.ASSISTANT_SESSION_EVENT_REGENERATE.format(id=session_id, event_id=event_id), payload
        )

    def feedback(self, session_id: str, event_id: int, value: str, note: Optional[str] = None) -> Any:
        payload: Dict[str, Any] = {"value": value}
        if note:
            payload["note"] = note
        return self.client.post(
            endpoints.ASSISTANT_SESSION_EVENT_FEEDBACK.format(id=session_id, event_id=event_id), payload
        )

    def analytics(self) -> Any:
        return self.client.get(endpoints.ASSISTANT_ANALYTICS)
