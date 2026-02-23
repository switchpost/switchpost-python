"""Step definitions for Task management (tasks.feature)."""

from __future__ import annotations

import contextlib
import json

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError
from switchpost.types.shared import RateLimit, RetryPolicy

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I create a task with the following properties:")
def create_task(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    # If required fields are missing, make a raw HTTP call so the API
    # returns 422 instead of Python raising TypeError.
    if "name" not in kwargs or "endpoint_url" not in kwargs:
        task = safe_call(
            ctx,
            lambda: _raw_create_task(ctx.client, kwargs),
            expected_status=201,
        )
    else:
        task = safe_call(ctx, ctx.client.tasks.create, expected_status=201, **kwargs)

    if task is not None:
        # Track the very first task for "delete the first created task" step
        if ctx.first_task is None:
            ctx.first_task = task
            ctx.first_task_id = task.id
        ctx.task = task
        ctx.task_id = task.id
        ctx.created_tasks.append(task.id)


def _raw_create_task(client, body: dict):
    """Send a raw POST /tasks with an arbitrary body dict.

    Used when required fields are deliberately missing to test API validation.
    """
    from switchpost.types.task import Task

    response = client._request("POST", "/tasks", json=body)
    return Task.model_validate(response.json())


@when("the task has a retry policy:")
def task_has_retry_policy(ctx: ScenarioContext, datatable) -> None:
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
    if task is not None:
        ctx.task = task


@when("the task has a rate limit:")
def task_has_rate_limit(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    rate = RateLimit(max_per_second=int(props["max_per_second"]))
    task = safe_call(
        ctx,
        ctx.client.tasks.update,
        ctx.task_id,
        rate_limit=rate,
        expected_status=200,
    )
    if task is not None:
        ctx.task = task


@when("I get the task by its ID")
def get_task_by_id(ctx: ScenarioContext) -> None:
    task = safe_call(ctx, ctx.client.tasks.get, ctx.task_id, expected_status=200)
    if task is not None:
        ctx.task = task


@when(parsers.parse('I get a task with ID "{task_id}"'))
def get_task_by_explicit_id(ctx: ScenarioContext, task_id: str) -> None:
    safe_call(ctx, ctx.client.tasks.get, task_id, expected_status=200)


@when("I update the task with the following properties:")
def update_task(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    task = safe_call(ctx, ctx.client.tasks.update, ctx.task_id, expected_status=200, **kwargs)
    if task is not None:
        ctx.task = task


@when("I delete the task")
def delete_task(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.tasks.delete, ctx.task_id, expected_status=204)


@when(parsers.parse('I delete a task with ID "{task_id}"'))
def delete_task_by_explicit_id(ctx: ScenarioContext, task_id: str) -> None:
    safe_call(ctx, ctx.client.tasks.delete, task_id, expected_status=204)


@when("I delete the first created task")
def delete_first_created_task(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.tasks.delete, ctx.first_task_id, expected_status=204)


@when("I delete the parent task")
def delete_parent_task(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.tasks.delete, ctx.parent_task_id, expected_status=204)


@when("I list tasks")
def list_tasks_default(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.tasks.list, expected_status=200)
    if result is not None:
        ctx.task_list = result


@when(parsers.parse("I list tasks with limit {limit:d} and offset {offset:d}"))
def list_tasks_with_params(ctx: ScenarioContext, limit: int, offset: int) -> None:
    result = safe_call(ctx, ctx.client.tasks.list, offset=offset, limit=limit, expected_status=200)
    if result is not None:
        ctx.task_list = result


@when(parsers.parse('I delete all tasks with name prefix "{prefix}"'))
def delete_tasks_by_prefix(ctx: ScenarioContext, prefix: str) -> None:
    page = ctx.client.tasks.list(limit=200)
    for task in page.data:
        if task.name.startswith(prefix):
            with contextlib.suppress(APIError):
                ctx.client.tasks.delete(task.id)


@when("I submit a run for the task with payload:")
def submit_run_with_payload(ctx: ScenarioContext, datatable) -> None:
    rows = list(datatable)
    # DataTable has header row: | key | value |
    # Build a dict from key/value rows (skip if first row is header)
    payload: dict = {}
    for row in rows:
        k, v = row[0], row[1]
        if k == "key" and v == "value":
            continue  # skip header
        payload[k] = parse_typed_value(v)

    run = safe_call(ctx, ctx.client.tasks.submit_run, ctx.task_id, payload=payload, expected_status=202)
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I submit a run for the task with:")
def submit_run_with_properties(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    if "payload" in props:
        try:
            kwargs["payload"] = json.loads(props["payload"])
        except json.JSONDecodeError:
            kwargs["payload"] = props["payload"]
    if "webhook_url" in props:
        kwargs["webhook_url"] = props["webhook_url"]

    run = safe_call(ctx, ctx.client.tasks.submit_run, ctx.task_id, expected_status=202, **kwargs)
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I submit a run for the task")
def submit_run_no_payload(ctx: ScenarioContext) -> None:
    run = safe_call(ctx, ctx.client.tasks.submit_run, ctx.task_id, expected_status=202)
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I list tasks using the new client")
def list_tasks_new_client(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.new_client.tasks.list, expected_status=200)
    if result is not None:
        ctx.task_list = result


# ---------------------------------------------------------------------------
# Then steps -- Task assertions
# ---------------------------------------------------------------------------


@then(parsers.parse('the task should have a "{prefix}" prefixed ID'))
def task_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.task is not None, "No task in context"
    assert ctx.task.id.startswith(prefix), f"Expected ID prefix {prefix!r}, got {ctx.task.id!r}"


@then(parsers.parse('the task name should be "{name}"'))
def task_name_is(ctx: ScenarioContext, name: str) -> None:
    assert ctx.task.name == name


@then(parsers.parse('the task endpoint_url should be "{url}"'))
def task_endpoint_url_is(ctx: ScenarioContext, url: str) -> None:
    assert ctx.task.endpoint_url == url


@then(parsers.parse("the task timeout_ms should be {value:d}"))
def task_timeout_ms_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.timeout_ms == value


@then("the task should have audit timestamps")
def task_has_audit(ctx: ScenarioContext) -> None:
    assert ctx.task.audit is not None
    assert ctx.task.audit.created_at is not None
    assert ctx.task.audit.updated_at is not None


@then(parsers.parse("the task max_concurrency should be {value:d}"))
def task_max_concurrency_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.max_concurrency == value


@then(parsers.parse("the task store_response should be {value}"))
def task_store_response_is(ctx: ScenarioContext, value: str) -> None:
    expected = value.lower() == "true"
    assert ctx.task.store_response == expected


@then(parsers.parse("the task result_ttl_seconds should be {value:d}"))
def task_result_ttl_seconds_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.result_ttl_seconds == value


@then(parsers.parse("the task success_codes should contain {code:d}"))
def task_success_codes_contains(ctx: ScenarioContext, code: int) -> None:
    assert code in ctx.task.success_codes


@then(parsers.parse("the task permanent_failure_codes should contain {code:d}"))
def task_permanent_failure_codes_contains(ctx: ScenarioContext, code: int) -> None:
    assert code in ctx.task.permanent_failure_codes


@then(parsers.parse("the task retry_policy max_attempts should be {value:d}"))
def task_retry_max_attempts(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.retry_policy is not None
    assert ctx.task.retry_policy.max_attempts == value


@then(parsers.parse("the task retry_policy initial_delay_ms should be {value:d}"))
def task_retry_initial_delay(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.retry_policy.initial_delay_ms == value


@then(parsers.parse("the task retry_policy multiplier should be {value:g}"))
def task_retry_multiplier(ctx: ScenarioContext, value: float) -> None:
    assert ctx.task.retry_policy.multiplier == value


@then(parsers.parse("the task retry_policy max_delay_ms should be {value:d}"))
def task_retry_max_delay(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.retry_policy.max_delay_ms == value


@then(parsers.parse("the task rate_limit max_per_second should be {value:d}"))
def task_rate_limit_max_per_second(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task.rate_limit is not None
    assert ctx.task.rate_limit.max_per_second == value


# -- Task list assertions ---------------------------------------------------


@then('the task list should have an "items" array')
def task_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.task_list is not None
    assert hasattr(ctx.task_list, "data")
    assert isinstance(ctx.task_list.data, list)


@then(parsers.parse('the task list should have a "total" count of at least {n:d}'))
def task_list_total_at_least(ctx: ScenarioContext, n: int) -> None:
    assert ctx.task_list.pagination.total >= n


@then('the task list should have a "total" count')
def task_list_has_total(ctx: ScenarioContext) -> None:
    assert ctx.task_list.pagination.total is not None


@then('the task list should have an "offset" value')
def task_list_has_offset(ctx: ScenarioContext) -> None:
    assert ctx.task_list.pagination.offset is not None


@then('the task list should have a "limit" value')
def task_list_has_limit(ctx: ScenarioContext) -> None:
    assert ctx.task_list.pagination.limit is not None


@then(parsers.parse('the task list "limit" should be {value:d}'))
def task_list_limit_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task_list.pagination.limit == value


@then(parsers.parse('the task list "offset" should be {value:d}'))
def task_list_offset_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.task_list.pagination.offset == value


@then(parsers.parse('the task list "items" should contain at most {n:d} tasks'))
def task_list_items_at_most(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.task_list.data) <= n


@then(parsers.parse('the task list "items" should contain at least {n:d} task'))
def task_list_items_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.task_list.data) >= n
