"""Usage resource."""

from __future__ import annotations

from .._requester import Requester
from ..models import Usage


class UsageResource:
    def __init__(self, requester: Requester) -> None:
        self._r = requester

    async def retrieve(self) -> Usage:
        """Retrieve usage statistics for the current API key."""
        data = await self._r.request("GET", "/v1/usage/")
        return Usage.from_dict(data)
