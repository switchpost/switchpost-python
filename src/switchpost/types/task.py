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
