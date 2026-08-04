"""Agents service."""
from __future__ import annotations

from typing import Any, Dict

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class AgentsService(BaseService):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client, endpoints.AGENTS, endpoints.AGENT_DETAIL)

    def preview(self, agent_id: Any, message: str) -> Any:
        return self.client.post(endpoints.AGENT_PREVIEW.format(id=agent_id), {"message": message})
