from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditInfo(BaseModel):
    """Tracks who created and last updated an entity, and when."""

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class CreatedInfo(BaseModel):
    """Tracks who created an entity and when."""

    created_at: datetime
    created_by: str


class RateLimit(BaseModel):
    """Throughput constraint for a task."""

    max_per_second: int


class RetryPolicy(BaseModel):
    """Exponential backoff configuration for task retries."""

    max_attempts: int
    initial_delay_ms: int
    multiplier: float
    max_delay_ms: int


class ErrorDetail(BaseModel):
    """A single validation or field-level error detail."""

    location: str | None = None
    message: str | None = None
    value: object | None = None


class ErrorModel(BaseModel):
    """RFC 7807 problem details error response."""

    type: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None
    instance: str | None = None
    errors: list[ErrorDetail] | None = None


class OffsetPaginationMeta(BaseModel):
    """Pagination metadata for offset-based list responses."""

    offset: int
    limit: int
    total: int


class CursorPaginationMeta(BaseModel):
    """Pagination metadata for cursor-based list responses."""

    has_more: bool
    next_cursor: str | None = None
    prev_cursor: str | None = None


__all__ = [
    "AuditInfo",
    "CreatedInfo",
    "CursorPaginationMeta",
    "ErrorDetail",
    "ErrorModel",
    "OffsetPaginationMeta",
    "RateLimit",
    "RetryPolicy",
]
