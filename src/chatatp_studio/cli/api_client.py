"""Thin HTTP client for the Studio backend.

This is the single seam between the CLI and the network. When this
codebase is merged into the official `chatatp-studio` SDK, replace the
body of the request methods with calls into the official SDK's own
transport and keep the same method signatures -- services and commands
do not need to change.
"""
from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .config import Config
from .exceptions import APIError, AuthenticationError

DEFAULT_TIMEOUT = 30


class APIClient:
    def __init__(self, config: Config, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.config = config
        self.timeout = timeout
        self.session = requests.Session()

    # -- internals -------------------------------------------------------
    def _url(self, path: str) -> str:
        base = self.config.api_url.rstrip("/") + "/"
        return urljoin(base, path.lstrip("/"))

    def _auth_header(self) -> Dict[str, str]:
        if self.config.access:
            return {"Authorization": f"Bearer {self.config.access}"}
        if self.config.token:
            return {"Authorization": f"Token {self.config.token}"}
        return {}

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        headers.update(self._auth_header())
        if extra:
            headers.update(extra)
        return headers

    def _handle_response(self, resp: requests.Response) -> Any:
        if resp.status_code == 204:
            return None
        try:
            payload = resp.json()
        except ValueError:
            payload = resp.text or None
        if resp.status_code == 401:
            raise AuthenticationError(
                "Not authenticated or session expired. Run `studio auth login`."
            )
        if not resp.ok:
            message = self._extract_message(payload) or f"Request failed with status {resp.status_code}"
            raise APIError(message, status_code=resp.status_code, payload=payload, url=resp.url)
        return payload

    @staticmethod
    def _extract_message(payload: Any) -> Optional[str]:
        if isinstance(payload, dict):
            for key in ("detail", "message", "error"):
                if key in payload:
                    return str(payload[key])
            # DRF validation errors: {"field": ["msg", ...]}
            parts = []
            for field, errors in payload.items():
                if isinstance(errors, list):
                    parts.append(f"{field}: {'; '.join(str(e) for e in errors)}")
                else:
                    parts.append(f"{field}: {errors}")
            if parts:
                return "; ".join(parts)
        if isinstance(payload, str):
            return payload
        return None

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry_on_401: bool = True,
    ) -> Any:
        url = self._url(path)
        headers = self._headers()
        if files is not None:
            # Let requests set the multipart content-type / boundary.
            resp = self.session.request(
                method, url, headers=headers, params=params, data=data, files=files, timeout=self.timeout
            )
        else:
            headers["Content-Type"] = "application/json"
            resp = self.session.request(
                method, url, headers=headers, params=params, json=json_body, timeout=self.timeout
            )

        if resp.status_code == 401 and retry_on_401 and self.config.refresh:
            if self._refresh_token():
                return self._request(
                    method,
                    path,
                    params=params,
                    json_body=json_body,
                    files=files,
                    data=data,
                    retry_on_401=False,
                )
        return self._handle_response(resp)

    def _refresh_token(self) -> bool:
        """Attempt to refresh the JWT access token. Returns True on success."""
        from . import endpoints

        try:
            resp = self.session.post(
                self._url(endpoints.AUTH_TOKEN_REFRESH),
                json={"refresh": self.config.refresh},
                timeout=self.timeout,
            )
        except requests.RequestException:
            return False
        if not resp.ok:
            return False
        try:
            payload = resp.json()
        except ValueError:
            return False
        access = payload.get("access")
        if not access:
            return False
        self.config.access = access
        self.config.save()
        return True

    # -- public verbs ------------------------------------------------------
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json_body: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        return self._request("POST", path, json_body=json_body, **kwargs)

    def put(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PUT", path, json_body=json_body)

    def patch(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PATCH", path, json_body=json_body)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def upload(self, path: str, file_path: str, field_name: str = "file", data: Optional[Dict[str, Any]] = None) -> Any:
        with open(file_path, "rb") as fh:
            files = {field_name: (file_path.split("/")[-1], fh)}
            return self._request("POST", path, files=files, data=data or {})
