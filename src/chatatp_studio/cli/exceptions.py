"""Exception types raised by the Studio CLI's internal API client."""
from __future__ import annotations

from typing import Any, Optional


class StudioError(Exception):
    """Base class for all studio_cli errors."""


class AuthenticationError(StudioError):
    """Raised when the user is not authenticated or credentials are invalid."""


class ConfigError(StudioError):
    """Raised for configuration file / profile problems."""


class APIError(StudioError):
    """Raised when the Studio backend returns an error response.

    Attributes:
        status_code: HTTP status code returned by the server (if any).
        payload: Parsed JSON error body (if any).
        url: The request URL that failed.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        payload: Optional[Any] = None,
        url: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload
        self.url = url

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        base = super().__str__()
        if self.status_code:
            return f"[{self.status_code}] {base}"
        return base
