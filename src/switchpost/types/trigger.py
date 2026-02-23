from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from switchpost.types.shared import AuditInfo


class Trigger(BaseModel):
    """A SwitchPost trigger definition."""

    id: str
    task_id: str
    type: str
    name: str
    enabled: bool
    audit: AuditInfo
    schedule: str | None = None
    timezone: str | None = None
    source_task_id: str | None = None
    on_status: str | None = None
    forward_result: bool | None = None
    default_payload: Any | None = None
    last_fired_at: datetime | None = None
    next_fire_at: datetime | None = None
    payload_mapping: str | None = None
    queue_adapter_type: str | None = None
    queue_adapter_config: Any | None = None


class CreateTriggerInputBody(BaseModel):
    """Request body for creating a trigger."""

    name: str
    type: str
    schedule: str | None = None
    timezone: str | None = None
    source_task_id: str | None = None
    on_status: str | None = None
    forward_result: bool | None = None
    default_payload: Any | None = None
    enabled: bool | None = None


class UpdateTriggerInputBody(BaseModel):
    """Request body for updating a trigger."""

    name: str | None = None
    schedule: str | None = None
    timezone: str | None = None
    source_task_id: str | None = None
    on_status: str | None = None
    forward_result: bool | None = None
    default_payload: Any | None = None
    enabled: bool | None = None


__all__ = [
    "CreateTriggerInputBody",
    "Trigger",
    "UpdateTriggerInputBody",
]
