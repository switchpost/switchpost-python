from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

from switchpost.types.shared import CursorPaginationMeta, OffsetPaginationMeta

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost

T = TypeVar("T", bound=BaseModel)


# ---------------------------------------------------------------------------
# Offset-based pagination (tasks, principals)
# ---------------------------------------------------------------------------


class SyncOffsetPage(Generic[T]):
    """A single page of offset-paginated results with auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Offset pagination metadata.
    """

    data: list[T]
    pagination: OffsetPaginationMeta

    def __init__(
        self,
        *,
        data: list[T],
        pagination: OffsetPaginationMeta,
        client: SwitchPost,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    def __iter__(self) -> Iterator[T]:
        """Iterate through all items across all pages (auto-pagination)."""
        page: SyncOffsetPage[T] = self
        while True:
            yield from page.data
            if page._is_last_page():
                break
            page = page._fetch_next_page()

    def _is_last_page(self) -> bool:
        if len(self.data) < self.pagination.limit:
            return True
        return self.pagination.offset + self.pagination.limit >= self.pagination.total

    def _fetch_next_page(self) -> SyncOffsetPage[T]:
        next_offset = self.pagination.offset + self.pagination.limit
        params = {**self._params, "offset": next_offset}
        response = self._client._request("GET", self._path, params=params)
        return _parse_sync_offset_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


class AsyncOffsetPage(Generic[T]):
    """A single page of offset-paginated results with async auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Offset pagination metadata.
    """

    data: list[T]
    pagination: OffsetPaginationMeta

    def __init__(
        self,
        *,
        data: list[T],
        pagination: OffsetPaginationMeta,
        client: AsyncSwitchPost,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    async def __aiter__(self) -> AsyncIterator[T]:
        """Iterate through all items across all pages (async auto-pagination)."""
        page: AsyncOffsetPage[T] = self
        while True:
            for item in page.data:
                yield item
            if page._is_last_page():
                break
            page = await page._fetch_next_page()

    def _is_last_page(self) -> bool:
        if len(self.data) < self.pagination.limit:
            return True
        return self.pagination.offset + self.pagination.limit >= self.pagination.total

    async def _fetch_next_page(self) -> AsyncOffsetPage[T]:
        next_offset = self.pagination.offset + self.pagination.limit
        params = {**self._params, "offset": next_offset}
        response = await self._client._request("GET", self._path, params=params)
        return _parse_async_offset_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


# ---------------------------------------------------------------------------
# Cursor-based pagination (runs, attempts)
# ---------------------------------------------------------------------------


class SyncCursorPage(Generic[T]):
    """A single page of cursor-paginated results with auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Cursor pagination metadata.
    """

    data: list[T]
    pagination: CursorPaginationMeta

    def __init__(
        self,
        *,
        data: list[T],
        pagination: CursorPaginationMeta,
        client: SwitchPost,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    def __iter__(self) -> Iterator[T]:
        """Iterate through all items across all pages (auto-pagination)."""
        page: SyncCursorPage[T] = self
        while True:
            yield from page.data
            if not page.pagination.has_more:
                break
            page = page._fetch_next_page()

    def _fetch_next_page(self) -> SyncCursorPage[T]:
        params = {**self._params, "after": self.pagination.next_cursor}
        params.pop("before", None)
        response = self._client._request("GET", self._path, params=params)
        return _parse_sync_cursor_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


class AsyncCursorPage(Generic[T]):
    """A single page of cursor-paginated results with async auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Cursor pagination metadata.
    """

    data: list[T]
    pagination: CursorPaginationMeta

    def __init__(
        self,
        *,
        data: list[T],
        pagination: CursorPaginationMeta,
        client: AsyncSwitchPost,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    async def __aiter__(self) -> AsyncIterator[T]:
        """Iterate through all items across all pages (async auto-pagination)."""
        page: AsyncCursorPage[T] = self
        while True:
            for item in page.data:
                yield item
            if not page.pagination.has_more:
                break
            page = await page._fetch_next_page()

    async def _fetch_next_page(self) -> AsyncCursorPage[T]:
        params = {**self._params, "after": self.pagination.next_cursor}
        params.pop("before", None)
        response = await self._client._request("GET", self._path, params=params)
        return _parse_async_cursor_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def _parse_sync_offset_page(
    *,
    data: dict[str, Any],
    client: SwitchPost,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> SyncOffsetPage[T]:
    """Parse an offset list response JSON into a SyncOffsetPage."""
    items = [model.model_validate(item) for item in (data.get("items") or [])]
    pagination = OffsetPaginationMeta(
        offset=data["offset"],
        limit=data["limit"],
        total=data["total"],
    )
    return SyncOffsetPage(
        data=items,
        pagination=pagination,
        client=client,
        path=path,
        params=params,
        model=model,
    )


def _parse_async_offset_page(
    *,
    data: dict[str, Any],
    client: AsyncSwitchPost,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> AsyncOffsetPage[T]:
    """Parse an offset list response JSON into an AsyncOffsetPage."""
    items = [model.model_validate(item) for item in (data.get("items") or [])]
    pagination = OffsetPaginationMeta(
        offset=data["offset"],
        limit=data["limit"],
        total=data["total"],
    )
    return AsyncOffsetPage(
        data=items,
        pagination=pagination,
        client=client,
        path=path,
        params=params,
        model=model,
    )


def _parse_sync_cursor_page(
    *,
    data: dict[str, Any],
    client: SwitchPost,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> SyncCursorPage[T]:
    """Parse a cursor list response JSON into a SyncCursorPage."""
    items = [model.model_validate(item) for item in (data.get("items") or [])]
    pagination = CursorPaginationMeta(
        has_more=data["has_more"],
        next_cursor=data.get("next_cursor"),
        prev_cursor=data.get("prev_cursor"),
    )
    return SyncCursorPage(
        data=items,
        pagination=pagination,
        client=client,
        path=path,
        params=params,
        model=model,
    )


def _parse_async_cursor_page(
    *,
    data: dict[str, Any],
    client: AsyncSwitchPost,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> AsyncCursorPage[T]:
    """Parse a cursor list response JSON into an AsyncCursorPage."""
    items = [model.model_validate(item) for item in (data.get("items") or [])]
    pagination = CursorPaginationMeta(
        has_more=data["has_more"],
        next_cursor=data.get("next_cursor"),
        prev_cursor=data.get("prev_cursor"),
    )
    return AsyncCursorPage(
        data=items,
        pagination=pagination,
        client=client,
        path=path,
        params=params,
        model=model,
    )
