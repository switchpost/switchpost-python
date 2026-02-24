# Copyright 2026 SwitchPost Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Any

from switchpost.types.settings import TenantSettings

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class SettingsResource:
    """Synchronous tenant settings API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def get(self) -> TenantSettings:
        """Get tenant settings."""
        response = self._client._request("GET", "/settings")
        return TenantSettings.model_validate(response.json())

    def update(
        self,
        *,
        default_max_attempts: int | None = None,
        default_initial_delay_ms: int | None = None,
        webhook_allowed_domains: list[str] | None = None,
        oauth_auto_provisioning: bool | None = None,
        api_rate_limit_per_minute: int | None = None,
        api_rate_limit_burst_size: int | None = None,
        max_batch_size: int | None = None,
        default_priority: int | None = None,
        default_result_ttl_seconds: int | None = None,
    ) -> TenantSettings:
        """Update tenant settings. This is a full replacement (PUT).

        Args:
            default_max_attempts: Default retry attempts for new tasks.
            default_initial_delay_ms: Default initial backoff delay in ms.
            webhook_allowed_domains: Allowed webhook delivery domains.
            oauth_auto_provisioning: Auto-create users on OAuth login.
            api_rate_limit_per_minute: API rate limit per minute.
            api_rate_limit_burst_size: API rate limit burst size.
            max_batch_size: Maximum batch submit size.
            default_priority: Default run priority.
            default_result_ttl_seconds: Default result TTL in seconds.
        """
        body = _update_body(
            default_max_attempts=default_max_attempts,
            default_initial_delay_ms=default_initial_delay_ms,
            webhook_allowed_domains=webhook_allowed_domains,
            oauth_auto_provisioning=oauth_auto_provisioning,
            api_rate_limit_per_minute=api_rate_limit_per_minute,
            api_rate_limit_burst_size=api_rate_limit_burst_size,
            max_batch_size=max_batch_size,
            default_priority=default_priority,
            default_result_ttl_seconds=default_result_ttl_seconds,
        )
        response = self._client._request("PUT", "/settings", json=body)
        return TenantSettings.model_validate(response.json())


class AsyncSettingsResource:
    """Asynchronous tenant settings API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def get(self) -> TenantSettings:
        """Get tenant settings."""
        response = await self._client._request("GET", "/settings")
        return TenantSettings.model_validate(response.json())

    async def update(
        self,
        *,
        default_max_attempts: int | None = None,
        default_initial_delay_ms: int | None = None,
        webhook_allowed_domains: list[str] | None = None,
        oauth_auto_provisioning: bool | None = None,
        api_rate_limit_per_minute: int | None = None,
        api_rate_limit_burst_size: int | None = None,
        max_batch_size: int | None = None,
        default_priority: int | None = None,
        default_result_ttl_seconds: int | None = None,
    ) -> TenantSettings:
        """Update tenant settings. This is a full replacement (PUT).

        Args:
            default_max_attempts: Default retry attempts for new tasks.
            default_initial_delay_ms: Default initial backoff delay in ms.
            webhook_allowed_domains: Allowed webhook delivery domains.
            oauth_auto_provisioning: Auto-create users on OAuth login.
            api_rate_limit_per_minute: API rate limit per minute.
            api_rate_limit_burst_size: API rate limit burst size.
            max_batch_size: Maximum batch submit size.
            default_priority: Default run priority.
            default_result_ttl_seconds: Default result TTL in seconds.
        """
        body = _update_body(
            default_max_attempts=default_max_attempts,
            default_initial_delay_ms=default_initial_delay_ms,
            webhook_allowed_domains=webhook_allowed_domains,
            oauth_auto_provisioning=oauth_auto_provisioning,
            api_rate_limit_per_minute=api_rate_limit_per_minute,
            api_rate_limit_burst_size=api_rate_limit_burst_size,
            max_batch_size=max_batch_size,
            default_priority=default_priority,
            default_result_ttl_seconds=default_result_ttl_seconds,
        )
        response = await self._client._request("PUT", "/settings", json=body)
        return TenantSettings.model_validate(response.json())


# --- Private helpers ---


def _update_body(
    *,
    default_max_attempts: int | None,
    default_initial_delay_ms: int | None,
    webhook_allowed_domains: list[str] | None,
    oauth_auto_provisioning: bool | None,
    api_rate_limit_per_minute: int | None,
    api_rate_limit_burst_size: int | None,
    max_batch_size: int | None,
    default_priority: int | None,
    default_result_ttl_seconds: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if default_max_attempts is not None:
        body["default_max_attempts"] = default_max_attempts
    if default_initial_delay_ms is not None:
        body["default_initial_delay_ms"] = default_initial_delay_ms
    if webhook_allowed_domains is not None:
        body["webhook_allowed_domains"] = webhook_allowed_domains
    if oauth_auto_provisioning is not None:
        body["oauth_auto_provisioning"] = oauth_auto_provisioning
    if api_rate_limit_per_minute is not None:
        body["api_rate_limit_per_minute"] = api_rate_limit_per_minute
    if api_rate_limit_burst_size is not None:
        body["api_rate_limit_burst_size"] = api_rate_limit_burst_size
    if max_batch_size is not None:
        body["max_batch_size"] = max_batch_size
    if default_priority is not None:
        body["default_priority"] = default_priority
    if default_result_ttl_seconds is not None:
        body["default_result_ttl_seconds"] = default_result_ttl_seconds
    return body
