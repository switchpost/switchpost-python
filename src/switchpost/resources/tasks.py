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

from typing import TYPE_CHECKING, Any, List

from switchpost._pagination import (
    AsyncCursorPage,
    AsyncOffsetPage,
    SyncCursorPage,
    SyncOffsetPage,
    _parse_async_cursor_page,
    _parse_async_offset_page,
    _parse_sync_cursor_page,
    _parse_sync_offset_page,
)
from switchpost.types.run import TaskRun
from switchpost.types.shared import RateLimit, RetryPolicy
from switchpost.types.task import Task

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class TasksResource:
    """Synchronous tasks API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> SyncOffsetPage[Task]:
        """List tasks for the tenant.

        Args:
            offset: Number of items to skip.
            limit: Maximum items to return (1-200).

        Returns:
            A page of tasks. Iterate directly to auto-paginate.
        """
        params = _list_params(offset=offset, limit=limit)
        response = self._client._request("GET", "/tasks", params=params)
        return _parse_sync_offset_page(
            data=response.json(),
            client=self._client,
            path="/tasks",
            params=params,
            model=Task,
        )

    def get(self, task_id: str) -> Task:
        """Get a task by ID.

        Args:
            task_id: Task ID (e.g. ``tsk_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/tasks/{task_id}")
        return Task.model_validate(response.json())

    def create(
        self,
        *,
        name: str,
        endpoint_url: str,
        timeout_ms: int | None = None,
        retry_policy: RetryPolicy | None = None,
        success_codes: List[int] | None = None,
        permanent_failure_codes: List[int] | None = None,
        store_response: bool | None = None,
        max_concurrency: int | None = None,
        rate_limit: RateLimit | None = None,
        result_ttl_seconds: int | None = None,
    ) -> Task:
        """Create a new task.

        Args:
            name: Task slug, unique per tenant. ``[a-z0-9\\-_]``, max 100 chars.
            endpoint_url: HTTPS endpoint URL to call, max 2048 chars.
            timeout_ms: Per-attempt timeout in ms (1-30000000). Default: 30000.
            retry_policy: Exponential backoff configuration.
            success_codes: HTTP status codes indicating success (1-20 elements).
            permanent_failure_codes: HTTP status codes that should not be retried.
            store_response: Whether to persist response bodies. Default: true.
            max_concurrency: Maximum concurrent runs (1-10000).
            rate_limit: Throughput constraint.
            result_ttl_seconds: Duration before stored results expire (60-31536000).
        """
        body = _create_body(
            name=name,
            endpoint_url=endpoint_url,
            timeout_ms=timeout_ms,
            retry_policy=retry_policy,
            success_codes=success_codes,
            permanent_failure_codes=permanent_failure_codes,
            store_response=store_response,
            max_concurrency=max_concurrency,
            rate_limit=rate_limit,
            result_ttl_seconds=result_ttl_seconds,
        )
        response = self._client._request("POST", "/tasks", json=body)
        return Task.model_validate(response.json())

    def update(
        self,
        task_id: str,
        *,
        endpoint_url: str | None = None,
        timeout_ms: int | None = None,
        retry_policy: RetryPolicy | None = None,
        success_codes: List[int] | None = None,
        permanent_failure_codes: List[int] | None = None,
        store_response: bool | None = None,
        max_concurrency: int | None = None,
        rate_limit: RateLimit | None = None,
        result_ttl_seconds: int | None = None,
    ) -> Task:
        """Partially update a task. Only provided fields are changed.

        Args:
            task_id: Task ID.
            endpoint_url: Updated HTTPS endpoint URL.
            timeout_ms: Updated per-attempt timeout in ms.
            retry_policy: Updated retry configuration.
            success_codes: Updated success status codes.
            permanent_failure_codes: Updated permanent failure codes.
            store_response: Updated response storage flag.
            max_concurrency: Updated concurrency limit.
            rate_limit: Updated rate limit configuration.
            result_ttl_seconds: Updated result TTL in seconds.
        """
        body = _update_body(
            endpoint_url=endpoint_url,
            timeout_ms=timeout_ms,
            retry_policy=retry_policy,
            success_codes=success_codes,
            permanent_failure_codes=permanent_failure_codes,
            store_response=store_response,
            max_concurrency=max_concurrency,
            rate_limit=rate_limit,
            result_ttl_seconds=result_ttl_seconds,
        )
        response = self._client._request("PATCH", f"/tasks/{task_id}", json=body)
        return Task.model_validate(response.json())

    def delete(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: Task ID.
        """
        self._client._request("DELETE", f"/tasks/{task_id}")

    def submit_run(
        self,
        task_id: str,
        *,
        payload: Any | None = None,
        webhook_url: str | None = None,
    ) -> TaskRun:
        """Submit a new task run.

        Args:
            task_id: Task ID.
            payload: JSON payload for the run. Max 1MB.
            webhook_url: Optional webhook URL to notify on completion.
        """
        body = _submit_run_body(payload=payload, webhook_url=webhook_url)
        response = self._client._request("POST", f"/tasks/{task_id}/runs", json=body)
        return TaskRun.model_validate(response.json())

    def list_runs(
        self,
        task_id: str,
        *,
        status: str | None = None,
        limit: int = 50,
        after: str | None = None,
        before: str | None = None,
    ) -> SyncCursorPage[TaskRun]:
        """List runs for a task.

        Args:
            task_id: Task ID.
            status: Filter by run status (PENDING, RUNNING, COMPLETED, FAILED, CANCELLED).
            limit: Maximum items to return (1-200).
            after: Opaque cursor for the next page.
            before: Opaque cursor for the previous page.
        """
        params = _cursor_params(status=status, limit=limit, after=after, before=before)
        path = f"/tasks/{task_id}/runs"
        response = self._client._request("GET", path, params=params)
        return _parse_sync_cursor_page(
            data=response.json(),
            client=self._client,
            path=path,
            params=params,
            model=TaskRun,
        )


class AsyncTasksResource:
    """Asynchronous tasks API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> AsyncOffsetPage[Task]:
        """List tasks for the tenant.

        Args:
            offset: Number of items to skip.
            limit: Maximum items to return (1-200).

        Returns:
            A page of tasks. Async-iterate directly to auto-paginate.
        """
        params = _list_params(offset=offset, limit=limit)
        response = await self._client._request("GET", "/tasks", params=params)
        return _parse_async_offset_page(
            data=response.json(),
            client=self._client,
            path="/tasks",
            params=params,
            model=Task,
        )

    async def get(self, task_id: str) -> Task:
        """Get a task by ID.

        Args:
            task_id: Task ID (e.g. ``tsk_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/tasks/{task_id}")
        return Task.model_validate(response.json())

    async def create(
        self,
        *,
        name: str,
        endpoint_url: str,
        timeout_ms: int | None = None,
        retry_policy: RetryPolicy | None = None,
        success_codes: List[int] | None = None,
        permanent_failure_codes: List[int] | None = None,
        store_response: bool | None = None,
        max_concurrency: int | None = None,
        rate_limit: RateLimit | None = None,
        result_ttl_seconds: int | None = None,
    ) -> Task:
        """Create a new task.

        Args:
            name: Task slug, unique per tenant.
            endpoint_url: HTTPS endpoint URL to call.
            timeout_ms: Per-attempt timeout in ms.
            retry_policy: Exponential backoff configuration.
            success_codes: HTTP status codes indicating success.
            permanent_failure_codes: HTTP status codes that should not be retried.
            store_response: Whether to persist response bodies.
            max_concurrency: Maximum concurrent runs.
            rate_limit: Throughput constraint.
            result_ttl_seconds: Duration before stored results expire.
        """
        body = _create_body(
            name=name,
            endpoint_url=endpoint_url,
            timeout_ms=timeout_ms,
            retry_policy=retry_policy,
            success_codes=success_codes,
            permanent_failure_codes=permanent_failure_codes,
            store_response=store_response,
            max_concurrency=max_concurrency,
            rate_limit=rate_limit,
            result_ttl_seconds=result_ttl_seconds,
        )
        response = await self._client._request("POST", "/tasks", json=body)
        return Task.model_validate(response.json())

    async def update(
        self,
        task_id: str,
        *,
        endpoint_url: str | None = None,
        timeout_ms: int | None = None,
        retry_policy: RetryPolicy | None = None,
        success_codes: List[int] | None = None,
        permanent_failure_codes: List[int] | None = None,
        store_response: bool | None = None,
        max_concurrency: int | None = None,
        rate_limit: RateLimit | None = None,
        result_ttl_seconds: int | None = None,
    ) -> Task:
        """Partially update a task. Only provided fields are changed.

        Args:
            task_id: Task ID.
            endpoint_url: Updated HTTPS endpoint URL.
            timeout_ms: Updated per-attempt timeout in ms.
            retry_policy: Updated retry configuration.
            success_codes: Updated success status codes.
            permanent_failure_codes: Updated permanent failure codes.
            store_response: Updated response storage flag.
            max_concurrency: Updated concurrency limit.
            rate_limit: Updated rate limit configuration.
            result_ttl_seconds: Updated result TTL in seconds.
        """
        body = _update_body(
            endpoint_url=endpoint_url,
            timeout_ms=timeout_ms,
            retry_policy=retry_policy,
            success_codes=success_codes,
            permanent_failure_codes=permanent_failure_codes,
            store_response=store_response,
            max_concurrency=max_concurrency,
            rate_limit=rate_limit,
            result_ttl_seconds=result_ttl_seconds,
        )
        response = await self._client._request("PATCH", f"/tasks/{task_id}", json=body)
        return Task.model_validate(response.json())

    async def delete(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: Task ID.
        """
        await self._client._request("DELETE", f"/tasks/{task_id}")

    async def submit_run(
        self,
        task_id: str,
        *,
        payload: Any | None = None,
        webhook_url: str | None = None,
    ) -> TaskRun:
        """Submit a new task run.

        Args:
            task_id: Task ID.
            payload: JSON payload for the run. Max 1MB.
            webhook_url: Optional webhook URL to notify on completion.
        """
        body = _submit_run_body(payload=payload, webhook_url=webhook_url)
        response = await self._client._request("POST", f"/tasks/{task_id}/runs", json=body)
        return TaskRun.model_validate(response.json())

    async def list_runs(
        self,
        task_id: str,
        *,
        status: str | None = None,
        limit: int = 50,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncCursorPage[TaskRun]:
        """List runs for a task.

        Args:
            task_id: Task ID.
            status: Filter by run status.
            limit: Maximum items to return (1-200).
            after: Opaque cursor for the next page.
            before: Opaque cursor for the previous page.
        """
        params = _cursor_params(status=status, limit=limit, after=after, before=before)
        path = f"/tasks/{task_id}/runs"
        response = await self._client._request("GET", path, params=params)
        return _parse_async_cursor_page(
            data=response.json(),
            client=self._client,
            path=path,
            params=params,
            model=TaskRun,
        )


# --- Private helpers ---


def _list_params(*, offset: int, limit: int) -> dict[str, Any]:
    return {"offset": offset, "limit": limit}


def _cursor_params(
    *,
    status: str | None,
    limit: int,
    after: str | None,
    before: str | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"limit": limit}
    if status is not None:
        params["status"] = status
    if after is not None:
        params["after"] = after
    if before is not None:
        params["before"] = before
    return params


def _create_body(
    *,
    name: str,
    endpoint_url: str,
    timeout_ms: int | None,
    retry_policy: RetryPolicy | None,
    success_codes: list[int] | None,
    permanent_failure_codes: list[int] | None,
    store_response: bool | None,
    max_concurrency: int | None,
    rate_limit: RateLimit | None,
    result_ttl_seconds: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name, "endpoint_url": endpoint_url}
    if timeout_ms is not None:
        body["timeout_ms"] = timeout_ms
    if retry_policy is not None:
        body["retry_policy"] = retry_policy.model_dump()
    if success_codes is not None:
        body["success_codes"] = success_codes
    if permanent_failure_codes is not None:
        body["permanent_failure_codes"] = permanent_failure_codes
    if store_response is not None:
        body["store_response"] = store_response
    if max_concurrency is not None:
        body["max_concurrency"] = max_concurrency
    if rate_limit is not None:
        body["rate_limit"] = rate_limit.model_dump()
    if result_ttl_seconds is not None:
        body["result_ttl_seconds"] = result_ttl_seconds
    return body


def _update_body(
    *,
    endpoint_url: str | None,
    timeout_ms: int | None,
    retry_policy: RetryPolicy | None,
    success_codes: list[int] | None,
    permanent_failure_codes: list[int] | None,
    store_response: bool | None,
    max_concurrency: int | None,
    rate_limit: RateLimit | None,
    result_ttl_seconds: int | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if endpoint_url is not None:
        body["endpoint_url"] = endpoint_url
    if timeout_ms is not None:
        body["timeout_ms"] = timeout_ms
    if retry_policy is not None:
        body["retry_policy"] = retry_policy.model_dump()
    if success_codes is not None:
        body["success_codes"] = success_codes
    if permanent_failure_codes is not None:
        body["permanent_failure_codes"] = permanent_failure_codes
    if store_response is not None:
        body["store_response"] = store_response
    if max_concurrency is not None:
        body["max_concurrency"] = max_concurrency
    if rate_limit is not None:
        body["rate_limit"] = rate_limit.model_dump()
    if result_ttl_seconds is not None:
        body["result_ttl_seconds"] = result_ttl_seconds
    return body


def _submit_run_body(
    *,
    payload: Any | None,
    webhook_url: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if payload is not None:
        body["payload"] = payload
    if webhook_url is not None:
        body["webhook_url"] = webhook_url
    return body
