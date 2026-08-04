"""Shared CLI context: config, API client, and lazily-constructed services."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .api_client import APIClient
from .config import Config
from .services.agents_service import AgentsService
from .services.assistant_service import AssistantService
from .services.auth_service import AuthService
from .services.http_api_service import HttpApiService
from .services.kb_service import KnowledgeBaseService
from .services.llm_service import LLMService
from .services.mcp_service import MCPService
from .services.platforms_service import PlatformsService
from .services.teams_service import TeamsService
from .services.users_service import UsersService


@dataclass
class CLIContext:
    config: Config
    client: APIClient
    output_format: str = "table"

    _auth: Optional[AuthService] = field(default=None, repr=False)
    _users: Optional[UsersService] = field(default=None, repr=False)
    _teams: Optional[TeamsService] = field(default=None, repr=False)
    _agents: Optional[AgentsService] = field(default=None, repr=False)
    _assistant: Optional[AssistantService] = field(default=None, repr=False)
    _mcp: Optional[MCPService] = field(default=None, repr=False)
    _http_api: Optional[HttpApiService] = field(default=None, repr=False)
    _llm: Optional[LLMService] = field(default=None, repr=False)
    _kb: Optional[KnowledgeBaseService] = field(default=None, repr=False)
    _platforms: Optional[PlatformsService] = field(default=None, repr=False)

    @property
    def auth(self) -> AuthService:
        self._auth = self._auth or AuthService(self.client)
        return self._auth

    @property
    def users(self) -> UsersService:
        self._users = self._users or UsersService(self.client)
        return self._users

    @property
    def teams(self) -> TeamsService:
        self._teams = self._teams or TeamsService(self.client)
        return self._teams

    @property
    def agents(self) -> AgentsService:
        self._agents = self._agents or AgentsService(self.client)
        return self._agents

    @property
    def assistant(self) -> AssistantService:
        self._assistant = self._assistant or AssistantService(self.client)
        return self._assistant

    @property
    def mcp(self) -> MCPService:
        self._mcp = self._mcp or MCPService(self.client)
        return self._mcp

    @property
    def http_api(self) -> HttpApiService:
        self._http_api = self._http_api or HttpApiService(self.client)
        return self._http_api

    @property
    def llm(self) -> LLMService:
        self._llm = self._llm or LLMService(self.client)
        return self._llm

    @property
    def kb(self) -> KnowledgeBaseService:
        self._kb = self._kb or KnowledgeBaseService(self.client)
        return self._kb

    @property
    def platforms(self) -> PlatformsService:
        self._platforms = self._platforms or PlatformsService(self.client)
        return self._platforms
