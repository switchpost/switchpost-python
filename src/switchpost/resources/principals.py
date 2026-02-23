from typing import TYPE_CHECKING, Any

from switchpost._pagination import AsyncOffsetPage, SyncOffsetPage, _parse_async_offset_page, _parse_sync_offset_page
from switchpost.types.principal import CreatePrincipalResponse, Principal

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class PrincipalsResource:
    """Synchronous principals API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> SyncOffsetPage[Principal]:
        """List principals for the tenant.

        Args:
            offset: Number of items to skip.
            limit: Maximum items to return (1-200).

        Returns:
            A page of principals. Iterate directly to auto-paginate.
        """
        params = _list_params(offset=offset, limit=limit)
        response = self._client._request("GET", "/principals", params=params)
        return _parse_sync_offset_page(
            data=response.json(),
            client=self._client,
            path="/principals",
            params=params,
            model=Principal,
        )

    def get(self, principal_id: str) -> Principal:
        """Get a principal by ID.

        Args:
            principal_id: Principal ID.
        """
        response = self._client._request("GET", f"/principals/{principal_id}")
        return Principal.model_validate(response.json())

    def create(
        self,
        *,
        type: str,
        name: str,
        email: str | None = None,
        oauth_provider: str | None = None,
        oauth_subject: str | None = None,
        expires_at: str | None = None,
    ) -> CreatePrincipalResponse:
        """Create a new principal.

        Args:
            type: Principal type: ``api_key`` or ``user``.
            name: Human-readable principal name.
            email: User email (user type only).
            oauth_provider: OAuth provider (user type only).
            oauth_subject: OAuth subject ID (user type only).
            expires_at: Optional expiration time (API key only).

        Returns:
            The created principal and, for API key principals, the raw API key.
        """
        body = _create_body(
            type=type,
            name=name,
            email=email,
            oauth_provider=oauth_provider,
            oauth_subject=oauth_subject,
            expires_at=expires_at,
        )
        response = self._client._request("POST", "/principals", json=body)
        return CreatePrincipalResponse.model_validate(response.json())

    def delete(self, principal_id: str) -> None:
        """Delete a principal.

        Args:
            principal_id: Principal ID.
        """
        self._client._request("DELETE", f"/principals/{principal_id}")


class AsyncPrincipalsResource:
    """Asynchronous principals API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> AsyncOffsetPage[Principal]:
        """List principals for the tenant.

        Args:
            offset: Number of items to skip.
            limit: Maximum items to return (1-200).

        Returns:
            A page of principals. Async-iterate directly to auto-paginate.
        """
        params = _list_params(offset=offset, limit=limit)
        response = await self._client._request("GET", "/principals", params=params)
        return _parse_async_offset_page(
            data=response.json(),
            client=self._client,
            path="/principals",
            params=params,
            model=Principal,
        )

    async def get(self, principal_id: str) -> Principal:
        """Get a principal by ID.

        Args:
            principal_id: Principal ID.
        """
        response = await self._client._request("GET", f"/principals/{principal_id}")
        return Principal.model_validate(response.json())

    async def create(
        self,
        *,
        type: str,
        name: str,
        email: str | None = None,
        oauth_provider: str | None = None,
        oauth_subject: str | None = None,
        expires_at: str | None = None,
    ) -> CreatePrincipalResponse:
        """Create a new principal.

        Args:
            type: Principal type: ``api_key`` or ``user``.
            name: Human-readable principal name.
            email: User email (user type only).
            oauth_provider: OAuth provider (user type only).
            oauth_subject: OAuth subject ID (user type only).
            expires_at: Optional expiration time (API key only).

        Returns:
            The created principal and, for API key principals, the raw API key.
        """
        body = _create_body(
            type=type,
            name=name,
            email=email,
            oauth_provider=oauth_provider,
            oauth_subject=oauth_subject,
            expires_at=expires_at,
        )
        response = await self._client._request("POST", "/principals", json=body)
        return CreatePrincipalResponse.model_validate(response.json())

    async def delete(self, principal_id: str) -> None:
        """Delete a principal.

        Args:
            principal_id: Principal ID.
        """
        await self._client._request("DELETE", f"/principals/{principal_id}")


# --- Private helpers ---


def _list_params(*, offset: int, limit: int) -> dict[str, Any]:
    return {"offset": offset, "limit": limit}


def _create_body(
    *,
    type: str,
    name: str,
    email: str | None,
    oauth_provider: str | None,
    oauth_subject: str | None,
    expires_at: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"type": type, "name": name}
    if email is not None:
        body["email"] = email
    if oauth_provider is not None:
        body["oauth_provider"] = oauth_provider
    if oauth_subject is not None:
        body["oauth_subject"] = oauth_subject
    if expires_at is not None:
        body["expires_at"] = expires_at
    return body
