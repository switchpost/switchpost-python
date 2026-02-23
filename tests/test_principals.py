from __future__ import annotations

import json

import httpx
import pytest
import respx
from conftest import error_response, offset_list_response, principal_json

from switchpost import NotFoundError, Principal, SwitchPost
from switchpost.types.principal import CreatePrincipalResponse


class TestPrincipalsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/principals").mock(
            return_value=httpx.Response(
                200, json=offset_list_response([principal_json(), principal_json(name="Other Key")])
            )
        )

        page = client.principals.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Principal)
        assert page.data[0].name == "Test API Key"
        assert page.data[1].name == "Other Key"
        assert page.pagination.offset == 0

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.get("/principals").mock(return_value=httpx.Response(200, json=offset_list_response([])))

        client.principals.list(offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestPrincipalsGet:
    def test_get_returns_principal(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/principals/prn_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=principal_json())
        )

        principal = client.principals.get("prn_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(principal, Principal)
        assert principal.id == "prn_4K7fR9pLm2nQwXvY8cJH3"
        assert principal.name == "Test API Key"
        assert principal.type == "api_key"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.get("/principals/prn_nonexistent00000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.principals.get("prn_nonexistent00000000")

        assert exc_info.value.status_code == 404


class TestPrincipalsCreate:
    def test_create_returns_response(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        mock_api.post("/principals").mock(
            return_value=httpx.Response(
                201,
                json={
                    "principal": principal_json(name="New Key"),
                    "api_key": "sp_test_new_key_abc123",
                },
            )
        )

        result = client.principals.create(type="api_key", name="New Key")

        assert isinstance(result, CreatePrincipalResponse)
        assert result.principal.name == "New Key"
        assert result.api_key == "sp_test_new_key_abc123"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.post("/principals").mock(
            return_value=httpx.Response(
                201,
                json={"principal": principal_json(), "api_key": None},
            )
        )

        client.principals.create(type="api_key", name="CI Key")

        body = json.loads(route.calls[0].request.content)
        assert body["type"] == "api_key"
        assert body["name"] == "CI Key"

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.post("/principals").mock(
            return_value=httpx.Response(
                201,
                json={"principal": principal_json(), "api_key": None},
            )
        )

        client.principals.create(type="user", name="Test User")

        body = json.loads(route.calls[0].request.content)
        assert body == {"type": "user", "name": "Test User"}
        assert "email" not in body


class TestPrincipalsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: SwitchPost) -> None:
        route = mock_api.delete("/principals/prn_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.principals.delete("prn_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncPrincipals:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.get("/principals").mock(
            return_value=httpx.Response(200, json=offset_list_response([principal_json()]))
        )

        page = await async_client.principals.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test API Key"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.get("/principals/prn_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=principal_json())
        )

        principal = await async_client.principals.get("prn_4K7fR9pLm2nQwXvY8cJH3")

        assert principal.name == "Test API Key"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        mock_api.post("/principals").mock(
            return_value=httpx.Response(
                201,
                json={"principal": principal_json(name="New"), "api_key": "sp_test_xyz"},
            )
        )

        result = await async_client.principals.create(type="api_key", name="New")

        assert result.principal.name == "New"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from switchpost import AsyncSwitchPost

        assert isinstance(async_client, AsyncSwitchPost)
        route = mock_api.delete("/principals/prn_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.principals.delete("prn_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
