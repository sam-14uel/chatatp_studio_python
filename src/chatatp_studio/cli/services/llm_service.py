"""LLM providers and provider-config service."""
from __future__ import annotations

from typing import Any

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class LLMService:
    def __init__(self, client: APIClient) -> None:
        self.client = client
        self.providers = BaseService(client, endpoints.LLM_PROVIDERS, endpoints.LLM_PROVIDER_DETAIL)
        self.configs = BaseService(client, endpoints.LLM_PROVIDER_CONFIGS, endpoints.LLM_PROVIDER_CONFIG_DETAIL)

    def provider_models(self, provider_id: Any) -> Any:
        return self.client.get(endpoints.LLM_PROVIDER_MODELS.format(id=provider_id))
