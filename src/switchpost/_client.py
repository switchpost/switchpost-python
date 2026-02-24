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

from typing import Any

import httpx

from switchpost._config import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    DEFAULT_VERSION,
    ClientConfig,
    resolve_access_token,
    resolve_api_key,
    resolve_base_url,
)
from switchpost._errors import ConnectionError as SwitchPostConnectionError
from switchpost._errors import _make_api_error
from switchpost._version import __version__
from switchpost.resources.admin import AdminResource, AsyncAdminResource
from switchpost.resources.attempts import AsyncAttemptsResource, AttemptsResource
from switchpost.resources.bindings import AsyncBindingsResource, BindingsResource
from switchpost.resources.principals import AsyncPrincipalsResource, PrincipalsResource
from switchpost.resources.runs import AsyncRunsResource, RunsResource
from switchpost.resources.settings import AsyncSettingsResource, SettingsResource
from switchpost.resources.tasks import AsyncTasksResource, TasksResource
from switchpost.resources.triggers import AsyncTriggersResource, TriggersResource
from switchpost.resources.webhooks import AsyncWebhooksResource, WebhooksResource


class _BaseClient:
    """Shared logic for sync and async SwitchPost clients."""

    _config: ClientConfig

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        access_token: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        version: str = DEFAULT_VERSION,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._config = ClientConfig(
            base_url=resolve_base_url(base_url),
            api_key=resolve_api_key(api_key),
            access_token=resolve_access_token(access_token),
            timeout=timeout,
            version=version,
            max_retries=max_retries,
        )

    @property
    def _default_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "SwitchPost-Version": self._config.version,
            "User-Agent": f"switchpost-python/{__version__}",
            "Accept": "application/json",
        }
        if self._config.api_key:
            headers["Authorization"] = f"ApiKey {self._config.api_key}"
        elif self._config.access_token:
            headers["Authorization"] = f"Bearer {self._config.access_token}"
        return headers

    @staticmethod
    def _process_response(response: httpx.Response) -> httpx.Response:
        """Check response status and raise the appropriate error on failure."""
        if response.is_success:
            return response
        raise _make_api_error(response)


class SwitchPost(_BaseClient):
    """Synchronous SwitchPost API client.

    Usage::

        from switchpost import SwitchPost

        client = SwitchPost(base_url="https://api.example.com", api_key="sp_...")
        tasks = client.tasks.list()

        # As a context manager
        with SwitchPost(base_url="https://api.example.com", api_key="sp_...") as client:
            task = client.tasks.get("tsk_...")
    """

    tasks: TasksResource
    triggers: TriggersResource
    runs: RunsResource
    attempts: AttemptsResource
    webhooks: WebhooksResource
    principals: PrincipalsResource
    bindings: BindingsResource
    settings: SettingsResource
    admin: AdminResource

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.Client(
            base_url=self._config.base_url,
            headers=self._default_headers,
            timeout=self._config.timeout,
        )
        self.tasks = TasksResource(self)
        self.triggers = TriggersResource(self)
        self.runs = RunsResource(self)
        self.attempts = AttemptsResource(self)
        self.webhooks = WebhooksResource(self)
        self.principals = PrincipalsResource(self)
        self.bindings = BindingsResource(self)
        self.settings = SettingsResource(self)
        self.admin = AdminResource(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Send a synchronous HTTP request and process the response."""
        try:
            response = self._http.request(method, path, params=params, json=json)
        except httpx.ConnectError as exc:
            raise SwitchPostConnectionError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise SwitchPostConnectionError(f"Request timed out: {exc}") from exc
        return self._process_response(response)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> SwitchPost:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncSwitchPost(_BaseClient):
    """Asynchronous SwitchPost API client.

    Usage::

        from switchpost import AsyncSwitchPost

        client = AsyncSwitchPost(base_url="https://api.example.com", api_key="sp_...")
        tasks = await client.tasks.list()

        # As an async context manager
        async with AsyncSwitchPost(base_url="https://api.example.com", api_key="sp_...") as client:
            task = await client.tasks.get("tsk_...")
    """

    tasks: AsyncTasksResource
    triggers: AsyncTriggersResource
    runs: AsyncRunsResource
    attempts: AsyncAttemptsResource
    webhooks: AsyncWebhooksResource
    principals: AsyncPrincipalsResource
    bindings: AsyncBindingsResource
    settings: AsyncSettingsResource
    admin: AsyncAdminResource

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            headers=self._default_headers,
            timeout=self._config.timeout,
        )
        self.tasks = AsyncTasksResource(self)
        self.triggers = AsyncTriggersResource(self)
        self.runs = AsyncRunsResource(self)
        self.attempts = AsyncAttemptsResource(self)
        self.webhooks = AsyncWebhooksResource(self)
        self.principals = AsyncPrincipalsResource(self)
        self.bindings = AsyncBindingsResource(self)
        self.settings = AsyncSettingsResource(self)
        self.admin = AsyncAdminResource(self)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Send an asynchronous HTTP request and process the response."""
        try:
            response = await self._http.request(method, path, params=params, json=json)
        except httpx.ConnectError as exc:
            raise SwitchPostConnectionError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise SwitchPostConnectionError(f"Request timed out: {exc}") from exc
        return self._process_response(response)

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncSwitchPost:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
