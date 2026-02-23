from __future__ import annotations

import os

import httpx
import pytest
import respx

from switchpost import (
    AsyncSwitchPost,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    SwitchPost,
    SwitchPostError,
)
from switchpost._errors import ConflictError, RateLimitError
from switchpost._errors import ConnectionError as SwitchPostConnectionError

BASE_URL = "https://api.test.switchpost.dev"


class TestClientConfig:
    def test_requires_base_url(self) -> None:
        """Client raises if no base_url and no SWITCHPOST_API_URL env var."""
        env = os.environ.pop("SWITCHPOST_API_URL", None)
        try:
            with pytest.raises(ValueError, match="base_url must be provided"):
                SwitchPost(api_key="sp_test")
        finally:
            if env is not None:
                os.environ["SWITCHPOST_API_URL"] = env

    def test_reads_base_url_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Client reads base_url from SWITCHPOST_API_URL env var."""
        monkeypatch.setenv("SWITCHPOST_API_URL", "https://env.example.com")
        client = SwitchPost(api_key="sp_test")
        assert client._config.base_url == "https://env.example.com"
        client.close()

    def test_explicit_base_url_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit base_url takes precedence over env var."""
        monkeypatch.setenv("SWITCHPOST_API_URL", "https://env.example.com")
        client = SwitchPost(base_url="https://explicit.example.com", api_key="sp_test")
        assert client._config.base_url == "https://explicit.example.com"
        client.close()

    def test_requires_auth(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Client raises if neither api_key nor access_token is provided."""
        monkeypatch.delenv("SWITCHPOST_API_KEY", raising=False)
        monkeypatch.delenv("SWITCHPOST_ACCESS_TOKEN", raising=False)
        with pytest.raises(ValueError, match="SWITCHPOST_API_KEY"):
            SwitchPost(base_url=BASE_URL)

    def test_api_key_auth(self) -> None:
        """Client sets Authorization: ApiKey header when api_key is provided."""
        client = SwitchPost(base_url=BASE_URL, api_key="sp_test_123")
        assert client._default_headers["Authorization"] == "ApiKey sp_test_123"
        client.close()

    def test_bearer_auth(self) -> None:
        """Client sets Authorization: Bearer header when access_token is provided."""
        client = SwitchPost(base_url=BASE_URL, access_token="jwt_token_here")
        assert client._default_headers["Authorization"] == "Bearer jwt_token_here"
        client.close()

    def test_api_key_takes_precedence(self) -> None:
        """Client uses ApiKey auth when both api_key and access_token are provided."""
        client = SwitchPost(base_url=BASE_URL, api_key="sp_key", access_token="jwt_token")
        assert client._default_headers["Authorization"] == "ApiKey sp_key"
        client.close()

    def test_version_header(self) -> None:
        """Client sets SwitchPost-Version header."""
        client = SwitchPost(base_url=BASE_URL, api_key="sp_test")
        assert "SwitchPost-Version" in client._default_headers
        client.close()

    def test_user_agent(self) -> None:
        """Client sets user agent to switchpost-python/{version}."""
        client = SwitchPost(base_url=BASE_URL, api_key="sp_test")
        assert client._default_headers["User-Agent"].startswith("switchpost-python/")
        client.close()

    def test_strips_trailing_slash(self) -> None:
        """Client strips trailing slash from base_url."""
        client = SwitchPost(base_url="https://api.example.com/", api_key="sp_test")
        assert client._config.base_url == "https://api.example.com"
        client.close()

    def test_reads_api_key_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Client reads api_key from SWITCHPOST_API_KEY env var."""
        monkeypatch.setenv("SWITCHPOST_API_KEY", "sp_env_key")
        client = SwitchPost(base_url=BASE_URL)
        assert client._default_headers["Authorization"] == "ApiKey sp_env_key"
        client.close()

    def test_reads_access_token_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Client reads access_token from SWITCHPOST_ACCESS_TOKEN env var."""
        monkeypatch.setenv("SWITCHPOST_ACCESS_TOKEN", "jwt_env_token")
        client = SwitchPost(base_url=BASE_URL)
        assert client._default_headers["Authorization"] == "Bearer jwt_env_token"
        client.close()

    def test_explicit_api_key_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit api_key takes precedence over SWITCHPOST_API_KEY env var."""
        monkeypatch.setenv("SWITCHPOST_API_KEY", "sp_env_key")
        client = SwitchPost(base_url=BASE_URL, api_key="sp_explicit_key")
        assert client._default_headers["Authorization"] == "ApiKey sp_explicit_key"
        client.close()

    def test_explicit_access_token_overrides_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit access_token takes precedence over SWITCHPOST_ACCESS_TOKEN env var."""
        monkeypatch.setenv("SWITCHPOST_ACCESS_TOKEN", "jwt_env_token")
        client = SwitchPost(base_url=BASE_URL, access_token="jwt_explicit_token")
        assert client._default_headers["Authorization"] == "Bearer jwt_explicit_token"
        client.close()

    def test_requires_auth_mentions_env_vars(self) -> None:
        """Error message mentions env var names when no auth is provided."""
        with pytest.raises(ValueError, match="SWITCHPOST_API_KEY"):
            SwitchPost(base_url=BASE_URL)


class TestErrorHandling:
    def test_400_raises_bad_request(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks/tsk_bad").mock(
                return_value=httpx.Response(
                    400, json={"status": 400, "title": "Bad Request", "detail": "Invalid task ID format."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
                with pytest.raises(BadRequestError) as exc_info:
                    client.tasks.get("tsk_bad")
                assert exc_info.value.status_code == 400

    def test_401_raises_authentication_error(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks").mock(
                return_value=httpx.Response(
                    401, json={"status": 401, "title": "Unauthorized", "detail": "Invalid API key."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_invalid") as client, pytest.raises(AuthenticationError):
                client.tasks.list()

    def test_404_raises_not_found(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks/tsk_missing").mock(
                return_value=httpx.Response(
                    404, json={"status": 404, "title": "Not Found", "detail": "Task not found."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
                with pytest.raises(NotFoundError) as exc_info:
                    client.tasks.get("tsk_missing")
                assert exc_info.value.message == "Task not found."

    def test_409_raises_conflict(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.post("/tasks").mock(
                return_value=httpx.Response(
                    409, json={"status": 409, "title": "Conflict", "detail": "Task already exists."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client, pytest.raises(ConflictError):
                client.tasks.create(name="dup", endpoint_url="https://example.com")

    def test_429_raises_rate_limit(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks").mock(
                return_value=httpx.Response(
                    429, json={"status": 429, "title": "Too Many Requests", "detail": "Rate limited."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client, pytest.raises(RateLimitError):
                client.tasks.list()

    def test_500_raises_internal_server_error(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks").mock(
                return_value=httpx.Response(
                    500, json={"status": 500, "title": "Internal Server Error", "detail": "Something went wrong."}
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client, pytest.raises(InternalServerError):
                client.tasks.list()

    def test_error_with_details(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.post("/tasks").mock(
                return_value=httpx.Response(
                    422,
                    json={
                        "status": 422,
                        "title": "Unprocessable Entity",
                        "detail": "Validation failed.",
                        "errors": [
                            {"location": "body.name", "message": "name is required", "value": None},
                        ],
                    },
                )
            )
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
                from switchpost._errors import UnprocessableEntityError

                with pytest.raises(UnprocessableEntityError) as exc_info:
                    client.tasks.create(name="", endpoint_url="https://example.com")
                assert exc_info.value.details is not None
                assert len(exc_info.value.details) == 1
                assert exc_info.value.details[0].location == "body.name"

    def test_non_json_error(self) -> None:
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/tasks").mock(return_value=httpx.Response(502, text="Bad Gateway"))
            with SwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
                from switchpost._errors import APIError

                with pytest.raises(APIError) as exc_info:
                    client.tasks.list()
                assert exc_info.value.status_code == 502
                assert "Bad Gateway" in exc_info.value.message


class TestContextManager:
    def test_sync_context_manager(self) -> None:
        with respx.mock(base_url=BASE_URL), SwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
            assert isinstance(client, SwitchPost)

    async def test_async_context_manager(self) -> None:
        with respx.mock(base_url=BASE_URL):
            async with AsyncSwitchPost(base_url=BASE_URL, api_key="sp_test") as client:
                assert isinstance(client, AsyncSwitchPost)


class TestInheritance:
    def test_all_errors_inherit_from_switchpost_error(self) -> None:
        assert issubclass(BadRequestError, SwitchPostError)
        assert issubclass(AuthenticationError, SwitchPostError)
        assert issubclass(NotFoundError, SwitchPostError)
        assert issubclass(ConflictError, SwitchPostError)
        assert issubclass(RateLimitError, SwitchPostError)
        assert issubclass(InternalServerError, SwitchPostError)
        assert issubclass(SwitchPostConnectionError, SwitchPostError)
