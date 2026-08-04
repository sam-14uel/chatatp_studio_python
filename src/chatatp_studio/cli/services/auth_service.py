"""Authentication and account/profile service."""
from __future__ import annotations

from typing import Any, Dict

from .. import endpoints
from ..api_client import APIClient


class AuthService:
    def __init__(self, client: APIClient) -> None:
        self.client = client

    def signup(self, email: str, password: str, name: str) -> Dict[str, Any]:
        return self.client.post(endpoints.AUTH_SIGNUP, {"email": email, "password": password, "name": name})

    def signin(self, email: str, password: str) -> Dict[str, Any]:
        return self.client.post(endpoints.AUTH_SIGNIN, {"email": email, "password": password})

    def signout(self) -> Any:
        return self.client.post(endpoints.AUTH_SIGNOUT)

    def forgot_password(self, email: str) -> Any:
        return self.client.post(endpoints.AUTH_FORGOT_PASSWORD, {"email": email})

    def reset_password(self, token: str, password: str) -> Any:
        return self.client.post(endpoints.AUTH_RESET_PASSWORD, {"token": token, "password": password})

    def me(self) -> Dict[str, Any]:
        return self.client.get(endpoints.AUTH_ME)

    def update_profile(self, **fields: Any) -> Dict[str, Any]:
        return self.client.patch(endpoints.AUTH_PROFILE, json_body=fields)

    def onboarding(self, **fields: Any) -> Dict[str, Any]:
        return self.client.post(endpoints.AUTH_ONBOARDING, fields)

    def oauth_providers(self) -> Any:
        return self.client.get(endpoints.AUTH_OAUTH_PROVIDERS)

    def oauth_start(self, provider: str) -> Any:
        return self.client.post(endpoints.AUTH_OAUTH_START.format(provider=provider))

    def token_refresh(self, refresh: str) -> Dict[str, Any]:
        return self.client.post(endpoints.AUTH_TOKEN_REFRESH, {"refresh": refresh})
