"""Agents resource."""

from __future__ import annotations

from .._requester import Requester
from ..models import Agent, Page


class AgentsResource:
    def __init__(self, requester: Requester) -> None:
        self._r = requester

    async def list(self) -> Page[Agent]:
        """List all agents accessible to the current API key."""
        data = await self._r.request("GET", "/v1/agents/")
        return Page.from_dict(data, Agent)

    async def retrieve(self, agent_id: int) -> Agent:
        """Retrieve a single agent by ID."""
        data = await self._r.request("GET", f"/v1/agents/{agent_id}/")
        return Agent.from_dict(data)
