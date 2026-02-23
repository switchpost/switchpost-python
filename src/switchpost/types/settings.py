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
