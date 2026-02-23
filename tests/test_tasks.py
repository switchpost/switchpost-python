from __future__ import annotations

import json

import httpx
import pytest
import respx
from conftest import cursor_list_response, error_response, offset_list_response, run_json, task_json

from switchpost import NotFoundError, SwitchPost, Task, TaskRun


class TestTasksList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/tasks").mock(
            return_value=httpx.Response(200, json=offset_list_response([task_json(), task_json(name="other-task")]))
        )

        page = client.tasks.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Task)
        assert page.data[0].name == "test-task"
        assert page.data[1].name == "other-task"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 50

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.get("/tasks").mock(return_value=httpx.Response(200, json=offset_list_response([])))

        client.tasks.list(offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestTasksGet:
    def test_get_returns_task(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=task_json()))

        task = client.tasks.get("tsk_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(task, Task)
        assert task.id == "tsk_4K7fR9pLm2nQwXvY8cJH3"
        assert task.name == "test-task"
        assert task.endpoint_url == "https://example.com/webhook"
        assert task.retry_policy.max_attempts == 3

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/tasks/tsk_nonexistent00000000").mock(return_value=httpx.Response(404, json=error_response()))

        with pytest.raises(NotFoundError) as exc_info:
            client.tasks.get("tsk_nonexistent00000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "The requested resource was not found."


class TestTasksCreate:
    def test_create_returns_task(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.post("/tasks").mock(return_value=httpx.Response(201, json=task_json(name="new-task")))

        task = client.tasks.create(name="new-task", endpoint_url="https://example.com/webhook")

        assert isinstance(task, Task)
        assert task.name == "new-task"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.post("/tasks").mock(return_value=httpx.Response(201, json=task_json()))

        client.tasks.create(
            name="my-task",
            endpoint_url="https://example.com/webhook",
            timeout_ms=5000,
            success_codes=[200, 201],
        )

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "my-task"
        assert body["endpoint_url"] == "https://example.com/webhook"
        assert body["timeout_ms"] == 5000
        assert body["success_codes"] == [200, 201]

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.post("/tasks").mock(return_value=httpx.Response(201, json=task_json()))

        client.tasks.create(name="my-task", endpoint_url="https://example.com/webhook")

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "my-task", "endpoint_url": "https://example.com/webhook"}


class TestTasksUpdate:
    def test_update_returns_task(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.patch("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=task_json(endpoint_url="https://new.example.com"))
        )

        task = client.tasks.update("tsk_4K7fR9pLm2nQwXvY8cJH3", endpoint_url="https://new.example.com")

        assert task.endpoint_url == "https://new.example.com"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.patch("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=task_json())
        )

        client.tasks.update("tsk_4K7fR9pLm2nQwXvY8cJH3", timeout_ms=10000)

        body = json.loads(route.calls[0].request.content)
        assert body == {"timeout_ms": 10000}
        assert "endpoint_url" not in body


class TestTasksDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.delete("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.tasks.delete("tsk_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestTasksSubmitRun:
    def test_submit_run_returns_task_run(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.post("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3/runs").mock(return_value=httpx.Response(202, json=run_json()))

        run = client.tasks.submit_run("tsk_4K7fR9pLm2nQwXvY8cJH3", payload={"key": "value"})

        assert isinstance(run, TaskRun)
        assert run.id == "run_4K7fR9pLm2nQwXvY8cJH3"
        assert run.status == "PENDING"

    def test_submit_run_sends_body(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.post("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3/runs").mock(
            return_value=httpx.Response(202, json=run_json())
        )

        client.tasks.submit_run(
            "tsk_4K7fR9pLm2nQwXvY8cJH3",
            payload={"key": "value"},
            webhook_url="https://example.com/callback",
        )

        body = json.loads(route.calls[0].request.content)
        assert body["payload"] == {"key": "value"}
        assert body["webhook_url"] == "https://example.com/callback"


class TestTasksListRuns:
    def test_list_runs_returns_cursor_page(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3/runs").mock(
            return_value=httpx.Response(200, json=cursor_list_response([run_json()]))
        )

        page = client.tasks.list_runs("tsk_4K7fR9pLm2nQwXvY8cJH3")

        assert len(page.data) == 1
        assert isinstance(page.data[0], TaskRun)
        assert not page.pagination.has_more


class TestAsyncTasks:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.get("/tasks").mock(return_value=httpx.Response(200, json=offset_list_response([task_json()])))

        page = await async_client.tasks.list()

        assert len(page.data) == 1
        assert page.data[0].name == "test-task"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.get("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=task_json()))

        task = await async_client.tasks.get("tsk_4K7fR9pLm2nQwXvY8cJH3")

        assert task.name == "test-task"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.post("/tasks").mock(return_value=httpx.Response(201, json=task_json(name="new-task")))

        task = await async_client.tasks.create(name="new-task", endpoint_url="https://example.com/webhook")

        assert task.name == "new-task"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        route = mock_api.delete("/tasks/tsk_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.tasks.delete("tsk_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
