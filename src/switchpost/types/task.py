from __future__ import annotations

from pydantic import BaseModel

from switchpost.types.shared import AuditInfo, RateLimit, RetryPolicy


class Task(BaseModel):
    """A SwitchPost task definition."""

    id: str
    name: str
    endpoint_url: str
    timeout_ms: int
    retry_policy: RetryPolicy
    success_codes: list[int] | None = None
    permanent_failure_codes: list[int] | None = None
    store_response: bool
    audit: AuditInfo
    max_concurrency: int | None = None
    rate_limit: RateLimit | None = None
    result_ttl_seconds: int | None = None


class CreateTaskInputBody(BaseModel):
    """Request body for creating a task."""

    name: str
    endpoint_url: str
    timeout_ms: int | None = None
    retry_policy: RetryPolicy | None = None
    success_codes: list[int] | None = None
    permanent_failure_codes: list[int] | None = None
    store_response: bool | None = None
    max_concurrency: int | None = None
    rate_limit: RateLimit | None = None
    result_ttl_seconds: int | None = None


class UpdateTaskInputBody(BaseModel):
    """Request body for updating a task."""

    endpoint_url: str | None = None
    timeout_ms: int | None = None
    retry_policy: RetryPolicy | None = None
    success_codes: list[int] | None = None
    permanent_failure_codes: list[int] | None = None
    store_response: bool | None = None
    max_concurrency: int | None = None
    rate_limit: RateLimit | None = None
    result_ttl_seconds: int | None = None


__all__ = [
    "CreateTaskInputBody",
    "Task",
    "UpdateTaskInputBody",
]
