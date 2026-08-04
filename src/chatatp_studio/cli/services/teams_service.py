"""Teams, members, and invitations service."""
from __future__ import annotations

from typing import Any, Dict

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class TeamsService(BaseService):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client, endpoints.TEAMS, endpoints.TEAM_DETAIL)

    def list_members(self, team_id: Any) -> Any:
        return self.client.get(endpoints.TEAM_MEMBERS.format(id=team_id))

    def add_member(self, team_id: Any, user: Any, role: str = "member") -> Any:
        return self.client.post(endpoints.TEAM_MEMBERS.format(id=team_id), {"user": user, "role": role})

    def remove_member(self, team_id: Any, user_id: Any) -> Any:
        return self.client.delete(endpoints.TEAM_MEMBER_DETAIL.format(id=team_id, user_id=user_id))

    def list_invitations(self, team_id: Any) -> Any:
        return self.client.get(endpoints.TEAM_INVITATIONS.format(id=team_id))

    def create_invitation(self, team_id: Any, email: str, role: str = "member") -> Any:
        return self.client.post(endpoints.TEAM_INVITATIONS.format(id=team_id), {"email": email, "role": role})

    def accept_invitation(self, token: str) -> Any:
        return self.client.post(endpoints.TEAM_INVITATION_ACCEPT.format(token=token))

    def decline_invitation(self, token: str) -> Any:
        return self.client.post(endpoints.TEAM_INVITATION_DECLINE.format(token=token))
