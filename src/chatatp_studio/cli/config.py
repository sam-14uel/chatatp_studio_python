"""Configuration and credential storage for the Studio CLI.

Configuration lives at ``~/.studio/config.json`` by default (override with
the ``STUDIO_CONFIG_PATH`` environment variable). It stores the API base
URL, the active team, and the token bundle returned by the authentication
endpoints (``access``/``refresh`` JWTs and/or a DRF ``token``).

Sensitive fields never get printed in full by the UI layer; see
``studio_cli.ui.mask_secret``.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_API_URL = "https://chatatp-agent-builder-backend.onrender.com"

CONFIG_DIR = Path(os.environ.get("STUDIO_CONFIG_DIR", str(Path.home() / ".studio")))
CONFIG_PATH = Path(os.environ.get("STUDIO_CONFIG_PATH", str(CONFIG_DIR / "config.json")))


@dataclass
class Config:
    api_url: str = field(default_factory=lambda: os.environ.get("STUDIO_API_URL", DEFAULT_API_URL))
    access: Optional[str] = None
    refresh: Optional[str] = None
    token: Optional[str] = None
    user_email: Optional[str] = None
    user_id: Optional[int] = None
    team_id: Optional[int] = None
    output_format: str = "table"  # table | json

    # -- persistence ---------------------------------------------------
    @classmethod
    def load(cls) -> "Config":
        if CONFIG_PATH.exists():
            try:
                data = json.loads(CONFIG_PATH.read_text())
            except (json.JSONDecodeError, OSError):
                data = {}
        else:
            data = {}
        known = {f: data.get(f) for f in cls.__dataclass_fields__ if f in data}
        cfg = cls(**known)
        # Environment variables always take precedence for the API URL and
        # an ad-hoc bearer token, which is convenient for CI usage.
        if os.environ.get("STUDIO_API_URL"):
            cfg.api_url = os.environ["STUDIO_API_URL"]
        if os.environ.get("STUDIO_TOKEN"):
            cfg.token = os.environ["STUDIO_TOKEN"]
        return cfg

    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2, sort_keys=True))
        try:
            os.chmod(CONFIG_PATH, 0o600)
        except OSError:
            pass

    def clear_credentials(self) -> None:
        self.access = None
        self.refresh = None
        self.token = None
        self.user_email = None
        self.user_id = None

    def is_authenticated(self) -> bool:
        return bool(self.access or self.token)

    def set(self, key: str, value: Any) -> None:
        if key not in self.__dataclass_fields__:
            raise KeyError(f"Unknown config key: {key}")
        setattr(self, key, value)

    def get(self, key: str) -> Any:
        if key not in self.__dataclass_fields__:
            raise KeyError(f"Unknown config key: {key}")
        return getattr(self, key)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
