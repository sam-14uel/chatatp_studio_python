"""MCP servers and connections service."""
from __future__ import annotations

from typing import Any, Dict

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class MCPService:
    def __init__(self, client: APIClient) -> None:
        self.client = client
        self.servers = BaseService(client, endpoints.MCP_SERVERS, endpoints.MCP_SERVER_DETAIL)
        self.connections = BaseService(client, endpoints.MCP_CONNECTIONS, endpoints.MCP_CONNECTION_DETAIL)

    def oauth_initiate(self, connection_id: Any) -> Any:
        return self.client.post(endpoints.MCP_OAUTH_INITIATE.format(id=connection_id))
