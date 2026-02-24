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

from typing import TYPE_CHECKING

from switchpost.types.run import TaskResultMeta, TaskRun

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class RunsResource:
    """Synchronous runs API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def get(self, run_id: str) -> TaskRun:
        """Get a run by ID.

        Args:
            run_id: Run ID.
        """
        response = self._client._request("GET", f"/runs/{run_id}")
        return TaskRun.model_validate(response.json())

    def cancel(self, run_id: str) -> TaskRun:
        """Cancel a running task run.

        Args:
            run_id: Run ID.
        """
        response = self._client._request("POST", f"/runs/{run_id}/cancel")
        return TaskRun.model_validate(response.json())

    def retry(self, run_id: str) -> TaskRun:
        """Retry a failed run.

        Args:
            run_id: Run ID.
        """
        response = self._client._request("POST", f"/runs/{run_id}/retry")
        return TaskRun.model_validate(response.json())

    def get_result(self, run_id: str) -> TaskResultMeta:
        """Get result metadata for a completed run.

        Args:
            run_id: Run ID.
        """
        response = self._client._request("GET", f"/runs/{run_id}/result")
        return TaskResultMeta.model_validate(response.json())


class AsyncRunsResource:
    """Asynchronous runs API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def get(self, run_id: str) -> TaskRun:
        """Get a run by ID.

        Args:
            run_id: Run ID.
        """
        response = await self._client._request("GET", f"/runs/{run_id}")
        return TaskRun.model_validate(response.json())

    async def cancel(self, run_id: str) -> TaskRun:
        """Cancel a running task run.

        Args:
            run_id: Run ID.
        """
        response = await self._client._request("POST", f"/runs/{run_id}/cancel")
        return TaskRun.model_validate(response.json())

    async def retry(self, run_id: str) -> TaskRun:
        """Retry a failed run.

        Args:
            run_id: Run ID.
        """
        response = await self._client._request("POST", f"/runs/{run_id}/retry")
        return TaskRun.model_validate(response.json())

    async def get_result(self, run_id: str) -> TaskResultMeta:
        """Get result metadata for a completed run.

        Args:
            run_id: Run ID.
        """
        response = await self._client._request("GET", f"/runs/{run_id}/result")
        return TaskResultMeta.model_validate(response.json())
