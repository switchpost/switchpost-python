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

from __future__ import annotations

from pydantic import BaseModel


class TenantSettings(BaseModel):
    """Tenant-level configuration settings."""

    default_max_attempts: int
    default_initial_delay_ms: int
    webhook_allowed_domains: list[str] | None = None
    oauth_auto_provisioning: bool
    api_rate_limit_per_minute: int
    api_rate_limit_burst_size: int
    max_batch_size: int
    default_priority: int
    default_result_ttl_seconds: int | None = None


class SystemSettings(BaseModel):
    """System-wide admin settings."""

    max_tasks_per_tenant: int
    max_concurrent_runs_per_tenant: int
    default_worker_concurrency: int
    run_archival_batch_size: int
    run_archival_after_days: int | None = None


__all__ = [
    "SystemSettings",
    "TenantSettings",
]
