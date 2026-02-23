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
