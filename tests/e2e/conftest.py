"""Shared fixtures and context for e2e pytest-bdd tests."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

import pytest

from switchpost import APIError, SwitchPost


@dataclass
class ScenarioContext:
    """Shared state between step definitions within a single scenario."""

    client: SwitchPost | None = None

    # Current resources
    task: Any = None
    task_id: str = ""
    trigger: Any = None
    trigger_id: str = ""
    run: Any = None
    run_id: str = ""
    attempt: Any = None
    attempt_id: str = ""
    webhook: Any = None
    webhook_id: str = ""
    principal: Any = None
    principal_id: str = ""
    principal_response: Any = None
    binding: Any = None
    binding_id: str = ""
    settings: Any = None
    saved_settings: Any = None

    # Secondary resources
    source_task: Any = None
    source_task_id: str = ""
    another_principal: Any = None
    another_principal_id: str = ""
    another_run: Any = None
    another_run_id: str = ""
    new_client: SwitchPost | None = None
    retried_run: Any = None

    # Lists / pagination
    task_list: Any = None
    trigger_list: Any = None
    run_list: Any = None
    attempt_list: Any = None
    webhook_list: Any = None
    principal_list: Any = None
    binding_list: Any = None
    next_cursor: str = ""

    # Error tracking
    last_error: Any = None
    last_status_code: int = 0
    error_response: dict = field(default_factory=dict)

    # Cleanup tracking
    created_tasks: list = field(default_factory=list)
    created_triggers: list = field(default_factory=list)
    created_principals: list = field(default_factory=list)
    created_bindings: list = field(default_factory=list)
    created_webhooks: list = field(default_factory=list)

    # Extra context references
    first_task: Any = None
    first_task_id: str = ""
    parent_task: Any = None
    parent_task_id: str = ""

    # Task used for pagination in attempts
    pagination_task: Any = None
    pagination_task_id: str = ""

    # Task used for retry scenario in runs
    retry_task: Any = None
    retry_task_id: str = ""

    # Task used for result scenario in runs
    result_task: Any = None
    result_task_id: str = ""

    # Result metadata (for get_result scenario)
    result_meta: Any = None

    # Newly created task (for trigger empty list scenario)
    new_task: Any = None
    new_task_id: str = ""


@pytest.fixture()
def ctx():
    """Per-scenario context with a SwitchPost client built from env vars."""
    base_url = os.environ.get("SWITCHPOST_API_URL", "http://localhost:8080")
    api_key = os.environ.get("SWITCHPOST_API_KEY", "")
    client = SwitchPost(base_url=base_url, api_key=api_key)
    context = ScenarioContext(client=client)
    yield context
    # Cleanup
    client.close()
    if context.new_client:
        context.new_client.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def safe_call(ctx: ScenarioContext, fn, *args, expected_status: int = 200, **kwargs):
    """Call *fn*, capturing any APIError into *ctx*.

    On success ``ctx.last_status_code`` is set to *expected_status* and the
    return value of *fn* is returned.  On error the ``APIError`` details are
    stored on the context and ``None`` is returned.
    """
    try:
        result = fn(*args, **kwargs)
        ctx.last_error = None
        ctx.last_status_code = expected_status
        ctx.error_response = {}
        return result
    except APIError as e:
        ctx.last_error = e
        ctx.last_status_code = e.status_code
        ctx.error_response = {
            "status": e.status_code,
            "title": e.title,
            "detail": e.message,
            "type": e.error_type,
            "errors": [
                {
                    "location": d.location,
                    "message": d.message,
                    "value": d.value,
                }
                for d in (e.details or [])
            ],
        }
        return None


def parse_table(datatable) -> dict[str, str]:
    """Parse a pytest-bdd DataTable (2-column key/value) into a dict."""
    result = {}
    for row in datatable:
        result[row[0]] = row[1]
    return result


def parse_typed_value(raw: str) -> Any:
    """Convert a raw string from a Gherkin table into a typed Python value.

    Handles booleans, ints, floats, JSON arrays/objects, and plain strings.
    """
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False

    # Try JSON (arrays, objects)
    if raw.startswith("[") or raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

    # Try int
    try:
        return int(raw)
    except ValueError:
        pass

    # Try float
    try:
        return float(raw)
    except ValueError:
        pass

    return raw


def wait_for_terminal_status(
    client: SwitchPost,
    run_id: str,
    *,
    timeout: float = 120,
    poll_interval: float = 2,
) -> Any:
    """Poll until the run reaches a terminal status or timeout is exceeded."""
    terminal = {"COMPLETED", "FAILED", "CANCELLED"}
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        run = client.runs.get(run_id)
        if run.status in terminal:
            return run
        time.sleep(poll_interval)
    raise TimeoutError(f"Run {run_id} did not reach terminal status within {timeout}s")
