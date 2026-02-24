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

from switchpost.types.shared import CreatedInfo


class TaskRun(BaseModel):
    """A SwitchPost task run."""

    id: str
    task_id: str
    trigger_id: str
    status: str
    max_attempts: int
    endpoint_url: str
    priority: int
    created: CreatedInfo
    max_concurrency: int | None = None
    rate_limit_max_per_second: int | None = None
    payload: Any | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    cancelled_by: str | None = None


class TaskRunAttempt(BaseModel):
    """A single execution attempt within a task run."""

    id: str
    run_id: str
    attempt_number: int
    status: str
    scheduled_at: datetime
    created_at: datetime
    created_by: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    response_status_code: int | None = None
    error_message: str | None = None
    request_headers: Any | None = None
    response_headers: Any | None = None


class TaskResultMeta(BaseModel):
    """Metadata for a stored task result."""

    id: str
    attempt_id: str
    run_id: str
    status_code: int
    blob_url: str
    stored_at: datetime
    content_type: str | None = None
    content_length: int | None = None
    response_headers: Any | None = None
    expires_at: datetime | None = None


class SubmitRunInputBody(BaseModel):
    """Request body for submitting a new task run."""

    payload: Any | None = None
    webhook_url: str | None = None


__all__ = [
    "SubmitRunInputBody",
    "TaskResultMeta",
    "TaskRun",
    "TaskRunAttempt",
]
