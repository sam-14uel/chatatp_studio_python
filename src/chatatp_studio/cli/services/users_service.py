"""Users and invitations service."""
from __future__ import annotations

from typing import Any

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class UsersService(BaseService):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client, endpoints.USERS, endpoints.USER_DETAIL)

    def list_invitations(self) -> Any:
        return self.client.get(endpoints.USER_INVITATIONS)

    def accept_invitation(self, token: str) -> Any:
        return self.client.post(endpoints.USER_INVITATION_ACCEPT.format(token=token))

    def decline_invitation(self, token: str) -> Any:
        return self.client.post(endpoints.USER_INVITATION_DECLINE.format(token=token))
