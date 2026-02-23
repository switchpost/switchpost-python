from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
import respx

from switchpost import AsyncSwitchPost, SwitchPost

BASE_URL = "https://api.test.switchpost.dev"


@pytest.fixture()
def mock_api() -> Iterator[respx.MockRouter]:
    with respx.mock(base_url=BASE_URL) as mock:
        yield mock


@pytest.fixture()
def client() -> Iterator[SwitchPost]:
    with SwitchPost(base_url=BASE_URL, api_key="sp_test_abc123") as c:
        yield c


@pytest.fixture()
def async_client() -> AsyncSwitchPost:
    return AsyncSwitchPost(base_url=BASE_URL, api_key="sp_test_abc123")


# --- Response factories ---


def task_json(
    *,
    id: str = "tsk_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "test-task",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "name": name,
        "endpoint_url": "https://example.com/webhook",
        "timeout_ms": 30000,
        "retry_policy": {
            "max_attempts": 3,
            "initial_delay_ms": 1000,
            "multiplier": 2.0,
            "max_delay_ms": 60000,
        },
        "success_codes": [200],
        "permanent_failure_codes": [400, 401],
        "store_response": True,
        "max_concurrency": None,
        "rate_limit": None,
        "result_ttl_seconds": None,
        "audit": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
            "updated_at": "2025-01-01T00:00:00Z",
            "updated_by": "prn_abc",
        },
        **overrides,
    }


def principal_json(
    *,
    id: str = "prn_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test API Key",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "type": "api_key",
        "name": name,
        "email": None,
        "oauth_provider": None,
        "oauth_subject": None,
        "key_prefix": "sp_test_",
        "expires_at": None,
        "last_seen_at": None,
        "audit": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
            "updated_at": "2025-01-01T00:00:00Z",
            "updated_by": "prn_abc",
        },
        **overrides,
    }


def run_json(
    *,
    id: str = "run_4K7fR9pLm2nQwXvY8cJH3",
    status: str = "PENDING",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "task_id": "tsk_4K7fR9pLm2nQwXvY8cJH3",
        "trigger_id": "trg_4K7fR9pLm2nQwXvY8cJH3",
        "status": status,
        "max_attempts": 3,
        "endpoint_url": "https://example.com/webhook",
        "priority": 0,
        "max_concurrency": None,
        "rate_limit_max_per_second": None,
        "payload": None,
        "started_at": None,
        "completed_at": None,
        "cancelled_at": None,
        "cancelled_by": None,
        "created": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
        },
        **overrides,
    }


def trigger_json(
    *,
    id: str = "trg_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test Trigger",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "task_id": "tsk_4K7fR9pLm2nQwXvY8cJH3",
        "type": "HTTP",
        "name": name,
        "enabled": True,
        "schedule": None,
        "timezone": None,
        "source_task_id": None,
        "on_status": None,
        "forward_result": None,
        "default_payload": None,
        "last_fired_at": None,
        "next_fire_at": None,
        "payload_mapping": None,
        "queue_adapter_type": None,
        "queue_adapter_config": None,
        "audit": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
            "updated_at": "2025-01-01T00:00:00Z",
            "updated_by": "prn_abc",
        },
        **overrides,
    }


def attempt_json(
    *,
    id: str = "att_4K7fR9pLm2nQwXvY8cJH3",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "run_id": "run_4K7fR9pLm2nQwXvY8cJH3",
        "attempt_number": 1,
        "status": "COMPLETED",
        "scheduled_at": "2025-01-01T00:00:00Z",
        "created_at": "2025-01-01T00:00:00Z",
        "created_by": "system",
        "started_at": "2025-01-01T00:00:01Z",
        "completed_at": "2025-01-01T00:00:02Z",
        "response_status_code": 200,
        "error_message": None,
        "request_headers": None,
        "response_headers": None,
        **overrides,
    }


def webhook_json(
    *,
    id: str = "whk_4K7fR9pLm2nQwXvY8cJH3",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "run_id": "run_4K7fR9pLm2nQwXvY8cJH3",
        "url": "https://example.com/callback",
        "secret_ref": None,
        "created": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
        },
        **overrides,
    }


def binding_json(
    *,
    id: str = "bnd_4K7fR9pLm2nQwXvY8cJH3",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "tenant_id": "tnt_4K7fR9pLm2nQwXvY8cJH3",
        "principal_id": "prn_4K7fR9pLm2nQwXvY8cJH3",
        "role": "admin",
        "resource_type": "tenant",
        "resource_id": "tnt_4K7fR9pLm2nQwXvY8cJH3",
        "created": {
            "created_at": "2025-01-01T00:00:00Z",
            "created_by": "prn_abc",
        },
        **overrides,
    }


def offset_list_response(
    items: list[dict[str, Any]],
    *,
    offset: int = 0,
    limit: int = 50,
    total: int | None = None,
) -> dict[str, Any]:
    return {
        "items": items,
        "offset": offset,
        "limit": limit,
        "total": total if total is not None else len(items),
    }


def cursor_list_response(
    items: list[dict[str, Any]],
    *,
    has_more: bool = False,
    next_cursor: str | None = None,
    prev_cursor: str | None = None,
) -> dict[str, Any]:
    return {
        "items": items,
        "has_more": has_more,
        "next_cursor": next_cursor,
        "prev_cursor": prev_cursor,
    }


def error_response(
    *,
    status: int = 404,
    title: str = "Not Found",
    detail: str = "The requested resource was not found.",
    type: str = "about:blank",
    errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "status": status,
        "title": title,
        "detail": detail,
        "type": type,
    }
    if errors is not None:
        body["errors"] = errors
    return body
