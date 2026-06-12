"""Low-level HTTP client wrapping httpx."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

import httpx

from .errors import NetworkError, TimeoutError, build_api_error

logger = logging.getLogger("chatatp")

DEFAULT_BASE_URL = "https://chatatp-agent-builder-backend.onrender.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
RETRY_INITIAL_DELAY = 0.5
RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


class Requester:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        debug: bool = False,
    ) -> None:
        self._api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._debug = debug

        if debug:
            logging.basicConfig()
            logger.setLevel(logging.DEBUG)

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            headers=self._auth_headers(),
        )

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        attempt = 0
        delay = RETRY_INITIAL_DELAY

        while True:
            logger.debug("→ %s %s", method, path)
            try:
                response = await self._client.request(
                    method,
                    path,
                    json=body,
                    params=clean_params or None,
                )
            except httpx.TimeoutException as exc:
                if attempt < self._max_retries:
                    logger.debug("timeout, retrying in %.1fs", delay)
                    await _sleep(delay)
                    delay *= 2
                    attempt += 1
                    continue
                raise TimeoutError(f"Request to {path} timed out.") from exc
            except httpx.RequestError as exc:
                if attempt < self._max_retries:
                    logger.debug("network error, retrying in %.1fs", delay)
                    await _sleep(delay)
                    delay *= 2
                    attempt += 1
                    continue
                raise NetworkError(f"Network request failed: {exc}") from exc

            logger.debug("← %s", response.status_code)

            if response.status_code == 204:
                return None

            body_json: dict[str, Any] = {}
            try:
                body_json = response.json()
            except Exception:
                pass

            if not response.is_success:
                request_id = response.headers.get("x-request-id")
                err = build_api_error(response.status_code, body_json, request_id)
                if response.status_code in RETRYABLE_STATUSES and attempt < self._max_retries:
                    logger.debug("retrying in %.1fs (attempt %d)", delay, attempt + 1)
                    await _sleep(delay)
                    delay *= 2
                    attempt += 1
                    continue
                raise err

            return body_json

    async def stream(
        self,
        path: str,
        body: Any,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Yield parsed SSE events as dicts with ``type`` and ``data`` keys."""
        headers = {**self._auth_headers(), "Accept": "text/event-stream"}
        buffer = ""

        async with self._client.stream(
            "POST",
            path,
            json=body,
            headers=headers,
            timeout=httpx.Timeout(self._timeout * 4),
        ) as response:
            if not response.is_success:
                raw = await response.aread()
                body_json: dict[str, Any] = {}
                try:
                    body_json = json.loads(raw)
                except Exception:
                    pass
                raise build_api_error(response.status_code, body_json)

            async for chunk in response.aiter_text():
                buffer += chunk
                *events, buffer = buffer.split("\n\n")
                for block in events:
                    parsed = _parse_sse_block(block)
                    if parsed:
                        logger.debug("← event: %s", parsed["type"])
                        yield parsed

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "Requester":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()


def _parse_sse_block(block: str) -> dict[str, Any] | None:
    event_type = ""
    data_str = ""
    for line in block.splitlines():
        if line.startswith("event:"):
            event_type = line[6:].strip()
        elif line.startswith("data:"):
            data_str = line[5:].strip()
    if not data_str:
        return None
    try:
        return {"type": event_type, "data": json.loads(data_str)}
    except json.JSONDecodeError:
        return {"type": event_type, "data": data_str}


async def _sleep(seconds: float) -> None:
    import asyncio
    await asyncio.sleep(seconds)
