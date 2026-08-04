"""Generic CRUD service used by every resource-specific service below."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..api_client import APIClient


class BaseService:
    """Wraps a REST collection at `collection_path` / `detail_path`.

    Resource-specific services subclass this to add custom actions (e.g.
    connect/disconnect, execute, search) while reusing list/get/create/
    update/delete for the standard CRUD surface.
    """

    def __init__(self, client: APIClient, collection_path: str, detail_path: Optional[str] = None) -> None:
        self.client = client
        self.collection_path = collection_path
        self.detail_path = detail_path or (collection_path.rstrip("/") + "/{id}/")

    def _detail(self, resource_id: Any, **extra: Any) -> str:
        return self.detail_path.format(id=resource_id, **extra)

    def list(self, **params: Any) -> Any:
        return self.client.get(self.collection_path, params=params or None)

    def get(self, resource_id: Any) -> Any:
        return self.client.get(self._detail(resource_id))

    def create(self, payload: Dict[str, Any]) -> Any:
        return self.client.post(self.collection_path, json_body=payload)

    def update(self, resource_id: Any, payload: Dict[str, Any], partial: bool = True) -> Any:
        if partial:
            return self.client.patch(self._detail(resource_id), json_body=payload)
        return self.client.put(self._detail(resource_id), json_body=payload)

    def delete(self, resource_id: Any) -> Any:
        return self.client.delete(self._detail(resource_id))
