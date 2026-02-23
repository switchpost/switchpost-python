"""Step definitions for Attempt management (attempts.feature)."""

from __future__ import annotations

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, safe_call

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I list attempts for the run")
def list_attempts(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.attempts.list, ctx.run_id, expected_status=200)
    if result is not None:
        ctx.attempt_list = result


@when(parsers.parse("I list attempts for the run with limit {limit:d}"))
def list_attempts_with_limit(ctx: ScenarioContext, limit: int) -> None:
    result = safe_call(ctx, ctx.client.attempts.list, ctx.run_id, limit=limit, expected_status=200)
    if result is not None:
        ctx.attempt_list = result
        if result.pagination.has_more and result.pagination.next_cursor:
            ctx.next_cursor = result.pagination.next_cursor


@when("I list attempts for the run using the next cursor")
def list_attempts_next_cursor(ctx: ScenarioContext) -> None:
    result = safe_call(
        ctx,
        ctx.client.attempts.list,
        ctx.run_id,
        after=ctx.next_cursor,
        expected_status=200,
    )
    if result is not None:
        ctx.attempt_list = result


@when("I get the first attempt by its ID")
def get_first_attempt(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    ctx.attempt_id = first.id
    attempt = safe_call(ctx, ctx.client.attempts.get, ctx.run_id, first.id, expected_status=200)
    if attempt is not None:
        ctx.attempt = attempt


@when(parsers.parse('I get attempt "{attempt_id}" for run "{run_id}"'))
def get_attempt_explicit(ctx: ScenarioContext, attempt_id: str, run_id: str) -> None:
    safe_call(ctx, ctx.client.attempts.get, run_id, attempt_id, expected_status=200)


@when("I submit a run for the pagination task")
def submit_run_pagination_task(ctx: ScenarioContext) -> None:
    task_id = ctx.pagination_task_id or ctx.task_id
    run = safe_call(
        ctx,
        ctx.client.tasks.submit_run,
        task_id,
        expected_status=202,
    )
    if run is not None:
        ctx.run = run
        ctx.run_id = run.id


@when("I delete the pagination task")
def delete_pagination_task(ctx: ScenarioContext) -> None:
    task_id = ctx.pagination_task_id or ctx.task_id
    safe_call(ctx, ctx.client.tasks.delete, task_id, expected_status=204)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('the attempt list should have an "items" array')
def attempt_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.attempt_list is not None
    assert isinstance(ctx.attempt_list.data, list)


@then('the attempt list should have a "has_more" boolean')
def attempt_list_has_has_more(ctx: ScenarioContext) -> None:
    assert isinstance(ctx.attempt_list.pagination.has_more, bool)


@then(parsers.parse('the attempt list "items" should contain at least {n:d} attempt'))
def attempt_list_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.attempt_list.data) >= n


@then(parsers.parse('the attempt list "items" should contain at most {n:d} attempt'))
def attempt_list_at_most(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.attempt_list.data) <= n


@then(parsers.parse('the attempt list "has_more" should be {value}'))
def attempt_list_has_more_is(ctx: ScenarioContext, value: str) -> None:
    expected = value.lower() == "true"
    assert ctx.attempt_list.pagination.has_more == expected


@then('the attempt list should have a "next_cursor" value')
def attempt_list_has_next_cursor(ctx: ScenarioContext) -> None:
    assert ctx.attempt_list.pagination.next_cursor is not None
    ctx.next_cursor = ctx.attempt_list.pagination.next_cursor


@then(parsers.parse('the first attempt should have an "{prefix}" prefixed ID'))
def first_attempt_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    first = ctx.attempt_list.data[0]
    assert first.id.startswith(prefix), f"Expected {prefix!r}, got {first.id!r}"


@then("the first attempt run_id should match the run ID")
def first_attempt_run_id(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    assert first.run_id == ctx.run_id


@then(parsers.parse("the first attempt attempt_number should be {n:d}"))
def first_attempt_number(ctx: ScenarioContext, n: int) -> None:
    first = ctx.attempt_list.data[0]
    assert first.attempt_number == n


@then("the first attempt should have a status")
def first_attempt_has_status(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    assert first.status is not None
    assert len(first.status) > 0


@then("the first attempt should have a scheduled_at timestamp")
def first_attempt_scheduled_at(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    assert first.scheduled_at is not None


@then("the first attempt should have a created_at timestamp")
def first_attempt_created_at(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    assert first.created_at is not None


@then("the first attempt should have a created_by value")
def first_attempt_created_by(ctx: ScenarioContext) -> None:
    first = ctx.attempt_list.data[0]
    assert first.created_by is not None
    assert len(first.created_by) > 0


@then("the attempt ID should match the first attempt")
def attempt_id_matches_first(ctx: ScenarioContext) -> None:
    assert ctx.attempt.id == ctx.attempt_id


@then("the attempt run_id should match the run ID")
def attempt_run_id_matches(ctx: ScenarioContext) -> None:
    assert ctx.attempt.run_id == ctx.run_id


@then(parsers.parse("the attempt attempt_number should be {n:d}"))
def attempt_number_is(ctx: ScenarioContext, n: int) -> None:
    assert ctx.attempt.attempt_number == n


@then("the attempt should have a started_at timestamp")
def attempt_has_started_at(ctx: ScenarioContext) -> None:
    assert ctx.attempt.started_at is not None


@then("the attempt should have a completed_at timestamp")
def attempt_has_completed_at(ctx: ScenarioContext) -> None:
    assert ctx.attempt.completed_at is not None


@then("the attempt response_status_code should be a valid HTTP status code")
def attempt_response_status_valid(ctx: ScenarioContext) -> None:
    assert ctx.attempt.response_status_code is not None
    assert 100 <= ctx.attempt.response_status_code < 600
