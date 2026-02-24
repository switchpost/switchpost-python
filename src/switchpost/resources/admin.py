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

from switchpost.types.settings import SystemSettings
from switchpost.types.tenant import CreateTenantResponse

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class AdminResource:
    """Synchronous admin API (system-level operations)."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def get_settings(self) -> SystemSettings:
        """Get system settings (admin only)."""
        response = self._client._request("GET", "/admin/settings")
        return SystemSettings.model_validate(response.json())

    def update_settings(
        self,
        *,
        max_tasks_per_tenant: int | None = None,
        max_concurrent_runs_per_tenant: int | None = None,
        default_worker_concurrency: int | None = None,
        run_archival_batch_size: int | None = None,
        run_archival_after_days: int | None = None,
    ) -> SystemSettings:
        """Update system settings (admin only). This is a full replacement (PUT).

        Args:
            max_tasks_per_tenant: Maximum tasks per tenant.
            max_concurrent_runs_per_tenant: Maximum concurrent runs per tenant.
            default_worker_concurrency: Default worker concurrency.
            run_archival_batch_size: Batch size for run archival.
            run_archival_after_days: Days before runs are archived.
        """
        body = _update_settings_body(
            max_tasks_per_tenant=max_tasks_per_tenant,
            max_concurrent_runs_per_tenant=max_concurrent_runs_per_tenant,
            default_worker_concurrency=default_worker_concurrency,
            run_archival_batch_size=run_archival_batch_size,
            run_archival_after_days=run_archival_after_days,
        )
        response = self._client._request("PUT", "/admin/settings", json=body)
        return SystemSettings.model_validate(response.json())

    def create_tenant(
        self,
        *,
        name: str,
        display_name: str,
    ) -> CreateTenantResponse:
        """Create a new tenant (admin only).

        Args:
            name: Tenant slug, globally unique. ``[a-z0-9\\-_]``, max 100 chars.
            display_name: Human-readable tenant label, max 200 chars.

        Returns:
            The created tenant, initial API key, and principal ID.
        """
        body: dict[str, Any] = {"name": name, "display_name": display_name}
        response = self._client._request("POST", "/admin/tenants", json=body)
        return CreateTenantResponse.model_validate(response.json())


class AsyncAdminResource:
    """Asynchronous admin API (system-level operations)."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def get_settings(self) -> SystemSettings:
        """Get system settings (admin only)."""
        response = await self._client._request("GET", "/admin/settings")
        return SystemSettings.model_validate(response.json())

    async def update_settings(
        self,
        *,
        max_tasks_per_tenant: int | None = None,
        max_concurrent_runs_per_tenant: int | None = None,
        default_worker_concurrency: int | None = None,
        run_archival_batch_size: int | None = None,
        run_archival_after_days: int | None = None,
    ) -> SystemSettings:
        """Update system settings (admin only). This is a full replacement (PUT).

        Args:
            max_tasks_per_tenant: Maximum tasks per tenant.
            max_concurrent_runs_per_tenant: Maximum concurrent runs per tenant.
            default_worker_concurrency: Default worker concurrency.
            run_archival_batch_size: Batch size for run archival.
            run_archival_after_days: Days before runs are archived.
        """
        body = _update_settings_body(
            max_tasks_per_tenant=max_tasks_per_tenant,
            max_concurrent_runs_per_tenant=max_concurrent_runs_per_tenant,
            default_worker_concurrency=default_worker_concurrency,
            run_archival_batch_size=run_archival_batch_size,
            run_archival_after_days=run_archival_after_days,
        )
        response = await self._client._request("PUT", "/admin/settings", json=body)
        return SystemSettings.model_validate(response.json())

    async def create_tenant(
        self,
        *,
        name: str,
        display_name: str,
    ) -> CreateTenantResponse:
        """Create a new tenant (admin only).

        Args:
            name: Tenant slug, globally unique.
            display_name: Human-readable tenant label, max 200 chars.

        Returns:
            The created tenant, initial API key, and principal ID.
        """
        body: dict[str, Any] = {"name": name, "display_name": display_name}
        response = await self._client._request("POST", "/admin/tenants", json=body)
        return CreateTenantResponse.model_validate(response.json())


# --- Private helpers ---


def _update_settings_body(
    *,
    max_tasks_per_tenant: int | None,
    max_concurrent_runs_per_tenant: int | None,
    default_worker_concurrency: int | None,
    run_archival_batch_size: int | None,
    run_archival_after_days: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if max_tasks_per_tenant is not None:
        body["max_tasks_per_tenant"] = max_tasks_per_tenant
    if max_concurrent_runs_per_tenant is not None:
        body["max_concurrent_runs_per_tenant"] = max_concurrent_runs_per_tenant
    if default_worker_concurrency is not None:
        body["default_worker_concurrency"] = default_worker_concurrency
    if run_archival_batch_size is not None:
        body["run_archival_batch_size"] = run_archival_batch_size
    if run_archival_after_days is not None:
        body["run_archival_after_days"] = run_archival_after_days
    return body
