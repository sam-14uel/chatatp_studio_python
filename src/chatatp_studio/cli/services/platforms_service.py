"""Messaging platform catalog and configs service."""
from __future__ import annotations

from typing import Any, Dict

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class PlatformsService:
    def __init__(self, client: APIClient) -> None:
        self.client = client
        self.configs = BaseService(client, endpoints.PLATFORM_CONFIGS, endpoints.PLATFORM_CONFIG_DETAIL)

    def list_catalog(self) -> Any:
        return self.client.get(endpoints.PLATFORM_CATALOG)

    def get_catalog_entry(self, platform_id: Any) -> Any:
        return self.client.get(endpoints.PLATFORM_CATALOG_DETAIL.format(id=platform_id))

    def connect(self, platform: Any, credentials: Dict[str, Any]) -> Any:
        return self.client.post(endpoints.PLATFORM_CONNECT, {"platform": platform, "credentials": credentials})

    def disconnect(self, platform: Any) -> Any:
        return self.client.post(endpoints.PLATFORM_DISCONNECT, {"platform": platform})
