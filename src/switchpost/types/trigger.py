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
