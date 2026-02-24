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

from switchpost._pagination import (
    AsyncCursorPage,
    SyncCursorPage,
    _parse_async_cursor_page,
    _parse_sync_cursor_page,
)
from switchpost.types.run import TaskRunAttempt

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class AttemptsResource:
    """Synchronous attempts API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(
        self,
        run_id: str,
        *,
        limit: int = 50,
        after: str | None = None,
        before: str | None = None,
    ) -> SyncCursorPage[TaskRunAttempt]:
        """List attempts for a run.

        Args:
            run_id: Parent run ID.
            limit: Maximum items to return (1-200).
            after: Opaque cursor for the next page.
            before: Opaque cursor for the previous page.
        """
        params = _list_params(limit=limit, after=after, before=before)
        path = f"/runs/{run_id}/attempts"
        response = self._client._request("GET", path, params=params)
        return _parse_sync_cursor_page(
            data=response.json(),
            client=self._client,
            path=path,
            params=params,
            model=TaskRunAttempt,
        )

    def get(self, run_id: str, attempt_id: str) -> TaskRunAttempt:
        """Get an attempt by ID.

        Args:
            run_id: Parent run ID.
            attempt_id: Attempt ID.
        """
        response = self._client._request("GET", f"/runs/{run_id}/attempts/{attempt_id}")
        return TaskRunAttempt.model_validate(response.json())


class AsyncAttemptsResource:
    """Asynchronous attempts API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(
        self,
        run_id: str,
        *,
        limit: int = 50,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncCursorPage[TaskRunAttempt]:
        """List attempts for a run.

        Args:
            run_id: Parent run ID.
            limit: Maximum items to return (1-200).
            after: Opaque cursor for the next page.
            before: Opaque cursor for the previous page.
        """
        params = _list_params(limit=limit, after=after, before=before)
        path = f"/runs/{run_id}/attempts"
        response = await self._client._request("GET", path, params=params)
        return _parse_async_cursor_page(
            data=response.json(),
            client=self._client,
            path=path,
            params=params,
            model=TaskRunAttempt,
        )

    async def get(self, run_id: str, attempt_id: str) -> TaskRunAttempt:
        """Get an attempt by ID.

        Args:
            run_id: Parent run ID.
            attempt_id: Attempt ID.
        """
        response = await self._client._request("GET", f"/runs/{run_id}/attempts/{attempt_id}")
        return TaskRunAttempt.model_validate(response.json())


# --- Private helpers ---


def _list_params(*, limit: int, after: str | None, before: str | None) -> dict[str, Any]:
    params: dict[str, Any] = {"limit": limit}
    if after is not None:
        params["after"] = after
    if before is not None:
        params["before"] = before
    return params
