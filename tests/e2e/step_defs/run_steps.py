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

"""Step definitions for Run management (runs.feature)."""

from __future__ import annotations

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_typed_value, safe_call, wait_for_terminal_status

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I get the run by its ID")
def get_run_by_id(ctx: ScenarioContext) -> None:
    run = safe_call(ctx, ctx.client.runs.get, ctx.run_id, expected_status=200)
    if run is not None:
        ctx.run = run


@when(parsers.parse('I get a run with ID "{run_id}"'))
def get_run_by_explicit_id(ctx: ScenarioContext, run_id: str) -> None:
    safe_call(ctx, ctx.client.runs.get, run_id, expected_status=200)


@when("I cancel the run")
def cancel_run(ctx: ScenarioContext) -> None:
    run = safe_call(ctx, ctx.client.runs.cancel, ctx.run_id, expected_status=200)
    if run is not None:
        ctx.run = run


@when("I cancel the run again")
def cancel_run_again(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.runs.cancel, ctx.run_id, expected_status=200)


@when(parsers.parse("I list runs for the task with limit {limit:d}"))
def list_runs_with_limit(ctx: ScenarioContext, limit: int) -> None:
    result = safe_call(
        ctx,
        ctx.client.tasks.list_runs,
        ctx.task_id,
        limit=limit,
        expected_status=200,
    )
    if result is not None:
        ctx.run_list = result
        if result.pagination.has_more and result.pagination.next_cursor:
            ctx.next_cursor = result.pagination.next_cursor


@when("I list runs for the task using the next cursor")
def list_runs_next_cursor(ctx: ScenarioContext) -> None:
    result = safe_call(
        ctx,
        ctx.client.tasks.list_runs,
        ctx.task_id,
        after=ctx.next_cursor,
        expected_status=200,
    )
    if result is not None:
        ctx.run_list = result


@when(parsers.parse('I list runs for the task with status "{status}"'))
def list_runs_by_status(ctx: ScenarioContext, status: str) -> None:
    result = safe_call(
        ctx,
        ctx.client.tasks.list_runs,
        ctx.task_id,
        status=status,
        expected_status=200,
    )
    if result is not None:
        ctx.run_list = result


@when("I list runs for the task")
def list_runs_default(ctx: ScenarioContext) -> None:
    result = safe_call(
        ctx,
        ctx.client.tasks.list_runs,
        ctx.task_id,
        expected_status=200,
    )
    if result is not None:
        ctx.run_list = result


@when("I wait for the run to reach a terminal status")
def wait_for_terminal(ctx: ScenarioContext) -> None:
    run = wait_for_terminal_status(ctx.client, ctx.run_id)
    ctx.run = run
    ctx.last_status_code = 200


@when("I submit a run for the retry task")
def submit_run_retry_task(ctx: ScenarioContext) -> None:
    # The retry task is the current task (set by the in-scenario Given step)
    task_id = ctx.retry_task_id or ctx.task_id
    run = safe_call(
        ctx,
        ctx.client.tasks.submit_run,
        task_id,
        expected_status=202,
    )
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I retry the run")
def retry_run(ctx: ScenarioContext) -> None:
    retried = safe_call(ctx, ctx.client.runs.retry, ctx.run_id, expected_status=202)
    if retried is not None:
        ctx.retried_run = retried


@when("I delete the retry task")
def delete_retry_task(ctx: ScenarioContext) -> None:
    task_id = ctx.retry_task_id or ctx.task_id
    safe_call(ctx, ctx.client.tasks.delete, task_id, expected_status=204)


@when("I submit a run for the result task with payload:")
def submit_run_result_task(ctx: ScenarioContext, datatable) -> None:
    rows = list(datatable)
    payload: dict = {}
    for row in rows:
        k, v = row[0], row[1]
        if k == "key" and v == "value":
            continue
        payload[k] = parse_typed_value(v)

    task_id = ctx.result_task_id or ctx.task_id
    run = safe_call(
        ctx,
        ctx.client.tasks.submit_run,
        task_id,
        payload=payload,
        expected_status=202,
    )
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I get the result for the run")
def get_result(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.runs.get_result, ctx.run_id, expected_status=200)
    if result is not None:
        ctx.result_meta = result


@when("I delete the result task")
def delete_result_task(ctx: ScenarioContext) -> None:
    task_id = ctx.result_task_id or ctx.task_id
    safe_call(ctx, ctx.client.tasks.delete, task_id, expected_status=204)


# -- Runs.feature Background "a task exists" that sets retry_task / result_task

# These are for the "Retry a failed run" and "Get result metadata" scenarios
# which use their own tasks (not the parent task from Background).
# The Given steps in given_steps.py handle "a task exists with ..."
# But runs.feature re-uses that same Given to create retry/result tasks mid-scenario.
# We handle this by tracking which task was just created.


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the run should have a "{prefix}" prefixed ID'))
def run_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.run is not None
    assert ctx.run.id.startswith(prefix), f"Expected {prefix!r}, got {ctx.run.id!r}"


@then(parsers.parse('the run status should be "{status}"'))
def run_status_is(ctx: ScenarioContext, status: str) -> None:
    assert ctx.run.status == status


@then("the run task_id should match the task ID")
def run_task_id_matches(ctx: ScenarioContext) -> None:
    assert ctx.run.task_id == ctx.task_id


@then("the run max_attempts should be a positive integer")
def run_max_attempts_positive(ctx: ScenarioContext) -> None:
    assert isinstance(ctx.run.max_attempts, int)
    assert ctx.run.max_attempts > 0


@then(parsers.parse('the run endpoint_url should be "{url}"'))
def run_endpoint_url_is(ctx: ScenarioContext, url: str) -> None:
    assert ctx.run.endpoint_url == url


@then("the run priority should be a non-negative integer")
def run_priority_nonneg(ctx: ScenarioContext) -> None:
    assert isinstance(ctx.run.priority, int)
    assert ctx.run.priority >= 0


@then("the run should have created info with created_at and created_by")
def run_has_created_info(ctx: ScenarioContext) -> None:
    assert ctx.run.created is not None
    assert ctx.run.created.created_at is not None
    assert ctx.run.created.created_by is not None


@then("the run ID should match the submitted run")
def run_id_matches_submitted(ctx: ScenarioContext) -> None:
    assert ctx.run.id == ctx.run_id


@then("the run cancelled_at should be present")
def run_cancelled_at_present(ctx: ScenarioContext) -> None:
    assert ctx.run.cancelled_at is not None


@then("the run cancelled_by should be present")
def run_cancelled_by_present(ctx: ScenarioContext) -> None:
    assert ctx.run.cancelled_by is not None


# -- Run list assertions ----------------------------------------------------


@then('the run list should have an "items" array')
def run_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.run_list is not None
    assert isinstance(ctx.run_list.data, list)


@then('the run list should have a "has_more" boolean')
def run_list_has_has_more(ctx: ScenarioContext) -> None:
    assert isinstance(ctx.run_list.pagination.has_more, bool)


@then(parsers.parse('the run list "items" should contain at most {n:d} runs'))
def run_list_at_most(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.run_list.data) <= n


@then(parsers.parse('the run list "items" should contain at least {n:d} run'))
def run_list_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.run_list.data) >= n


@then("if has_more is true then next_cursor should be present")
def run_list_cursor_check(ctx: ScenarioContext) -> None:
    if ctx.run_list.pagination.has_more:
        assert ctx.run_list.pagination.next_cursor is not None
        ctx.next_cursor = ctx.run_list.pagination.next_cursor


@then(parsers.parse('every run in the list should have status "{status}"'))
def every_run_has_status(ctx: ScenarioContext, status: str) -> None:
    for run in ctx.run_list.data:
        assert run.status == status


# -- Retry assertions -------------------------------------------------------


@then(parsers.parse('the retried run should have a new "{prefix}" prefixed ID'))
def retried_run_prefixed(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.retried_run is not None
    assert ctx.retried_run.id.startswith(prefix)


@then("the retried run ID should differ from the original run")
def retried_run_differs(ctx: ScenarioContext) -> None:
    assert ctx.retried_run.id != ctx.run_id


# -- Result assertions ------------------------------------------------------


@then('the result should have an "id" string')
def result_has_id(ctx: ScenarioContext) -> None:
    result = getattr(ctx, "result_meta", None)
    assert result is not None
    assert isinstance(result.id, str)
    assert len(result.id) > 0


@then(parsers.parse('the result attempt_id should have an "{prefix}" prefix'))
def result_attempt_id_prefix(ctx: ScenarioContext, prefix: str) -> None:
    result = getattr(ctx, "result_meta", None)
    assert result.attempt_id.startswith(prefix)


@then("the result run_id should match the run ID")
def result_run_id_matches(ctx: ScenarioContext) -> None:
    result = getattr(ctx, "result_meta", None)
    assert result.run_id == ctx.run_id


@then("the result status_code should be a valid HTTP status code")
def result_status_code_valid(ctx: ScenarioContext) -> None:
    result = getattr(ctx, "result_meta", None)
    assert 100 <= result.status_code < 600


@then("the result blob_url should be a URL string")
def result_blob_url_is_url(ctx: ScenarioContext) -> None:
    result = getattr(ctx, "result_meta", None)
    assert result.blob_url.startswith("http")


@then("the result stored_at should be a timestamp")
def result_stored_at_timestamp(ctx: ScenarioContext) -> None:
    result = getattr(ctx, "result_meta", None)
    assert result.stored_at is not None
