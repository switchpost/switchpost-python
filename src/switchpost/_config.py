from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_TIMEOUT = 60.0
DEFAULT_VERSION = "0.0.0"
DEFAULT_MAX_RETRIES = 2


@dataclass(frozen=True)
class ClientConfig:
    """Internal configuration for the SwitchPost API client."""

    base_url: str
    api_key: str | None = None
    access_token: str | None = None
    timeout: float = DEFAULT_TIMEOUT
    version: str = DEFAULT_VERSION
    max_retries: int = DEFAULT_MAX_RETRIES

    def __post_init__(self) -> None:
        if not self.api_key and not self.access_token:
            raise ValueError(
                "Authentication is required. Provide 'api_key' or 'access_token', "
                "or set the SWITCHPOST_API_KEY or SWITCHPOST_ACCESS_TOKEN environment variable."
            )


def resolve_base_url(base_url: str | None) -> str:
    """Resolve the base URL from the parameter or SWITCHPOST_API_URL env var."""
    if base_url is not None:
        return base_url.rstrip("/")
    env_url = os.environ.get("SWITCHPOST_API_URL")
    if env_url:
        return env_url.rstrip("/")
    raise ValueError(
        "A base_url must be provided either as a parameter or via the SWITCHPOST_API_URL environment variable. "
        "SwitchPost is self-hosted and has no default API URL."
    )


def resolve_api_key(api_key: str | None) -> str | None:
    """Resolve the API key from the parameter or SWITCHPOST_API_KEY env var."""
    if api_key is not None:
        return api_key
    return os.environ.get("SWITCHPOST_API_KEY") or None


def resolve_access_token(access_token: str | None) -> str | None:
    """Resolve the access token from the parameter or SWITCHPOST_ACCESS_TOKEN env var."""
    if access_token is not None:
        return access_token
    return os.environ.get("SWITCHPOST_ACCESS_TOKEN") or None
