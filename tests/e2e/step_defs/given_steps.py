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

"""Given step definitions shared across all features."""

from __future__ import annotations

from pytest_bdd import given, parsers
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError, SwitchPost
from switchpost.types.shared import RetryPolicy

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_or_replace_task(client: SwitchPost, kwargs: dict):
    """Create a task; if 409 (duplicate name) delete the existing one first."""
    try:
        return client.tasks.create(**kwargs)
    except APIError as e:
        if e.status_code != 409:
            raise
    # 409: find and delete the existing task, then retry
    name = kwargs.get("name", "")
    page = client.tasks.list(limit=200)
    for task in page.data:
        if task.name == name:
            client.tasks.delete(task.id)
            break
    return client.tasks.create(**kwargs)


def _create_or_replace_principal(client: SwitchPost, kwargs: dict):
    """Create a principal; if 409 (duplicate name) delete existing first."""
    try:
        return client.principals.create(**kwargs)
    except APIError as e:
        if e.status_code != 409:
            raise
    name = kwargs.get("name", "")
    page = client.principals.list(limit=200)
    for prn in page.data:
        if prn.name == name:
            client.principals.delete(prn.id)
            break
    return client.principals.create(**kwargs)


# -- Background steps -------------------------------------------------------


@given("a SwitchPost client with valid credentials", target_fixture="ctx")
def given_valid_client(ctx: ScenarioContext) -> ScenarioContext:
    """The default ctx fixture already carries a valid client."""
    return ctx


@given("a SwitchPost client with no credentials", target_fixture="ctx")
def given_no_credentials_client(ctx: ScenarioContext) -> ScenarioContext:
    """Create a client with an empty API key (should be rejected)."""
    base_url = ctx.client._config.base_url if ctx.client else "http://localhost:8080"
    ctx.client.close()
    ctx.client = SwitchPost(base_url=base_url, api_key="no-credentials-placeholder")
    return ctx


@given(parsers.parse('a SwitchPost client with API key "{api_key}"'), target_fixture="ctx")
def given_client_with_api_key(ctx: ScenarioContext, api_key: str) -> ScenarioContext:
    base_url = ctx.client._config.base_url if ctx.client else "http://localhost:8080"
    ctx.client.close()
    ctx.client = SwitchPost(base_url=base_url, api_key=api_key)
    return ctx


# -- Resource setup steps ---------------------------------------------------


@given("a task exists with the following properties:")
def given_task_exists(ctx: ScenarioContext, datatable) -> None:
    """Create a task from datatable and store it as the current/parent task.

    If a task with the same name already exists (409), delete it first and
    retry so that Background steps succeed across independent scenarios.
    """
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    task = _create_or_replace_task(ctx.client, kwargs)
    assert task is not None, f"Failed to create task: {ctx.last_error}"
    ctx.last_status_code = 201
    ctx.last_error = None
    ctx.error_response = {}
    ctx.task = task
    ctx.task_id = task.id
    # Only set parent_task on the first call (from Background).
    # In-scenario Given steps should NOT overwrite parent_task_id.
    if not ctx.parent_task_id:
        ctx.parent_task = task
        ctx.parent_task_id = task.id
    ctx.created_tasks.append(task.id)


@given("another task exists with the following properties:")
def given_another_task_exists(ctx: ScenarioContext, datatable) -> None:
    """Create a secondary (source) task."""
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    task = _create_or_replace_task(ctx.client, kwargs)
    assert task is not None, f"Failed to create source task: {ctx.last_error}"
    ctx.source_task = task
    ctx.source_task_id = task.id
    ctx.created_tasks.append(task.id)


@given("the task has a retry policy:")
def given_task_retry_policy(ctx: ScenarioContext, datatable) -> None:
    """Update the current task to include a retry policy."""
    props = parse_table(datatable)
    policy = RetryPolicy(
        max_attempts=int(props["max_attempts"]),
        initial_delay_ms=int(props["initial_delay_ms"]),
        multiplier=float(props["multiplier"]),
        max_delay_ms=int(props["max_delay_ms"]),
    )
    task = safe_call(
        ctx,
        ctx.client.tasks.update,
        ctx.task_id,
        retry_policy=policy,
        expected_status=200,
    )
    assert task is not None, f"Failed to update task retry policy: {ctx.last_error}"
    ctx.task = task


@given("a run has been submitted for the task")
def given_run_submitted(ctx: ScenarioContext) -> None:
    """Submit a run for the current task."""
    run = safe_call(
        ctx,
        ctx.client.tasks.submit_run,
        ctx.task_id,
        expected_status=202,
    )
    assert run is not None, f"Failed to submit run: {ctx.last_error}"
    ctx.run = run
    ctx.run_id = run.id


@given("another run has been submitted for the task")
def given_another_run_submitted(ctx: ScenarioContext) -> None:
    """Submit another run for the current task."""
    run = safe_call(
        ctx,
        ctx.client.tasks.submit_run,
        ctx.task_id,
        expected_status=202,
    )
    assert run is not None, f"Failed to submit another run: {ctx.last_error}"
    ctx.another_run = run
    ctx.another_run_id = run.id


@given("a principal exists with the following properties:")
def given_principal_exists(ctx: ScenarioContext, datatable) -> None:
    """Create a principal and store it as current."""
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    resp = _create_or_replace_principal(ctx.client, kwargs)
    assert resp is not None, f"Failed to create principal: {ctx.last_error}"
    ctx.principal_response = resp
    ctx.principal = resp.principal
    ctx.principal_id = resp.principal.id
    ctx.created_principals.append(resp.principal.id)


@given("another principal exists with the following properties:")
def given_another_principal_exists(ctx: ScenarioContext, datatable) -> None:
    """Create another principal."""
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    resp = _create_or_replace_principal(ctx.client, kwargs)
    assert resp is not None, f"Failed to create another principal: {ctx.last_error}"
    ctx.another_principal = resp.principal
    ctx.another_principal_id = resp.principal.id
    ctx.created_principals.append(resp.principal.id)
