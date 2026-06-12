"""SDK-specific exception classes."""

from __future__ import annotations

from typing import Any


class ChatATPError(Exception):
    """Base error for all ChatATP SDK errors."""

    status_code: int | None
    request_id: str | None
    payload: Any

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.payload = payload


class AuthenticationError(ChatATPError):
    """Raised when authentication fails (HTTP 401)."""

    def __init__(self, message: str = "Invalid or revoked API key.", **kwargs: Any) -> None:
        super().__init__(message, status_code=401, **kwargs)


class PermissionError(ChatATPError):  # noqa: A001
    """Raised when scope or ownership check fails (HTTP 403)."""

    def __init__(self, message: str = "Missing scope or owner permission.", **kwargs: Any) -> None:
        super().__init__(message, status_code=403, **kwargs)


class ValidationError(ChatATPError):
    """Raised for invalid request data (HTTP 400)."""

    def __init__(self, message: str = "Invalid request.", **kwargs: Any) -> None:
        super().__init__(message, status_code=400, **kwargs)


class RateLimitError(ChatATPError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""

    def __init__(self, message: str = "Rate limit exceeded.", **kwargs: Any) -> None:
        super().__init__(message, status_code=429, **kwargs)


class NotFoundError(ChatATPError):
    """Raised when a requested resource does not exist (HTTP 404)."""

    def __init__(self, message: str = "Resource not found.", **kwargs: Any) -> None:
        super().__init__(message, status_code=404, **kwargs)


class ServerError(ChatATPError):
    """Raised for 5xx server errors."""

    def __init__(self, message: str = "Internal server error.", **kwargs: Any) -> None:
        super().__init__(message, status_code=500, **kwargs)


class NetworkError(ChatATPError):
    """Raised when a network-level failure occurs."""


class TimeoutError(NetworkError):
    """Raised when a request times out."""


_STATUS_MAP: dict[int, type[ChatATPError]] = {
    400: ValidationError,
    401: AuthenticationError,
    403: PermissionError,
    404: NotFoundError,
    429: RateLimitError,
}


def build_api_error(
    status: int,
    body: dict[str, Any],
    request_id: str | None = None,
) -> ChatATPError:
    """Map an HTTP status code to an appropriate SDK exception."""
    message = body.get("detail") or f"HTTP {status}"
    kwargs: dict[str, Any] = {"status_code": status, "request_id": request_id, "payload": body}

    if status in _STATUS_MAP:
        return _STATUS_MAP[status](message, **kwargs)
    if status >= 500:
        return ServerError(message, **kwargs)
    return ChatATPError(message, **kwargs)
