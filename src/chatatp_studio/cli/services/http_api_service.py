"""HTTP API tools and connections service."""
from __future__ import annotations

from typing import Any, Dict, Optional

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class HttpApiService:
    def __init__(self, client: APIClient) -> None:
        self.client = client
        self.tools = BaseService(client, endpoints.HTTP_API_TOOLS, endpoints.HTTP_API_TOOL_DETAIL)
        self.connections = BaseService(client, endpoints.HTTP_API_CONNECTIONS, endpoints.HTTP_API_CONNECTION_DETAIL)

    def execute(self, connection_id: Any, body: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.post(endpoints.HTTP_API_CONNECTION_EXECUTE.format(id=connection_id), body or {})

    def oauth_initiate(self, connection_id: Any) -> Any:
        return self.client.post(endpoints.HTTP_API_OAUTH_INITIATE.format(id=connection_id))
