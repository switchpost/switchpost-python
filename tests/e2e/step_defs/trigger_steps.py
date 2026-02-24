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

"""Step definitions for Trigger management (triggers.feature)."""

from __future__ import annotations

import contextlib

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I create a trigger on the task with the following properties:")
def create_trigger(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        if key == "source_task_id" and raw_val == "<source_task_id>":
            kwargs[key] = ctx.source_task_id
        else:
            kwargs[key] = parse_typed_value(raw_val)

    # If required fields are missing, use raw HTTP call for API validation
    if "name" not in kwargs or "type" not in kwargs:
        trigger = safe_call(
            ctx,
            lambda: _raw_create_trigger(ctx.client, ctx.task_id, kwargs),
            expected_status=201,
        )
    else:
        trigger = safe_call(
            ctx,
            ctx.client.triggers.create,
            ctx.task_id,
            expected_status=201,
            **kwargs,
        )

    if trigger is not None:
        ctx.trigger = trigger
        ctx.trigger_id = trigger.id
        ctx.created_triggers.append((ctx.task_id, trigger.id))


def _raw_create_trigger(client, task_id: str, body: dict):
    """Raw POST for trigger creation when required fields may be missing."""
    from switchpost.types.trigger import Trigger

    response = client._request("POST", f"/tasks/{task_id}/triggers", json=body)
    return Trigger.model_validate(response.json())


@when("I create a trigger on the first task with the following properties:")
def create_trigger_on_first_task(ctx: ScenarioContext, datatable) -> None:
    """Create a trigger on the parent/first task (used in EVENT trigger scenario)."""
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        if key == "source_task_id" and raw_val == "<source_task_id>":
            kwargs[key] = ctx.source_task_id
        else:
            kwargs[key] = parse_typed_value(raw_val)

    # The "first task" in triggers.feature context is the parent_task
    task_id = ctx.parent_task_id or ctx.task_id
    trigger = safe_call(
        ctx,
        ctx.client.triggers.create,
        task_id,
        expected_status=201,
        **kwargs,
    )
    if trigger is not None:
        ctx.trigger = trigger
        ctx.trigger_id = trigger.id
        ctx.created_triggers.append((task_id, trigger.id))


@when("I get the trigger by its ID")
def get_trigger(ctx: ScenarioContext) -> None:
    task_id = ctx.parent_task_id or ctx.task_id
    trigger = safe_call(
        ctx,
        ctx.client.triggers.get,
        task_id,
        ctx.trigger_id,
        expected_status=200,
    )
    if trigger is not None:
        ctx.trigger = trigger


@when(parsers.parse('I get trigger "{trigger_id}" on task "{task_id}"'))
def get_trigger_explicit(ctx: ScenarioContext, trigger_id: str, task_id: str) -> None:
    safe_call(ctx, ctx.client.triggers.get, task_id, trigger_id, expected_status=200)


@when("I update the trigger with the following properties:")
def update_trigger(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    task_id = ctx.parent_task_id or ctx.task_id
    trigger = safe_call(
        ctx,
        ctx.client.triggers.update,
        task_id,
        ctx.trigger_id,
        expected_status=200,
        **kwargs,
    )
    if trigger is not None:
        ctx.trigger = trigger


@when("I delete the trigger")
def delete_trigger(ctx: ScenarioContext) -> None:
    task_id = ctx.parent_task_id or ctx.task_id
    safe_call(ctx, ctx.client.triggers.delete, task_id, ctx.trigger_id, expected_status=204)


@when("I delete the source task")
def delete_source_task(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.tasks.delete, ctx.source_task_id, expected_status=204)


@when("I list triggers for the task")
def list_triggers(ctx: ScenarioContext) -> None:
    task_id = ctx.parent_task_id or ctx.task_id
    result = safe_call(ctx, ctx.client.triggers.list, task_id, expected_status=200)
    if result is not None:
        ctx.trigger_list = result


@when("I list triggers for the newly created task")
def list_triggers_new_task(ctx: ScenarioContext) -> None:
    # This uses the task created in the "Given a task exists ..." step WITHIN
    # the scenario (which overwrites ctx.task_id).  The parent_task is set from
    # the Background; the scenario step creates a *new* task, and we need its id.
    result = safe_call(ctx, ctx.client.triggers.list, ctx.task_id, expected_status=200)
    if result is not None:
        ctx.trigger_list = result


@when(parsers.parse('I delete all triggers with name prefix "{prefix}"'))
def delete_triggers_by_prefix(ctx: ScenarioContext, prefix: str) -> None:
    task_id = ctx.parent_task_id or ctx.task_id
    triggers = ctx.client.triggers.list(task_id)
    for trg in triggers:
        if trg.name.startswith(prefix):
            with contextlib.suppress(APIError):
                ctx.client.triggers.delete(task_id, trg.id)


@when("I delete the newly created task")
def delete_newly_created_task(ctx: ScenarioContext) -> None:
    """Delete the task that was created in a Given step within the scenario body."""
    safe_call(ctx, ctx.client.tasks.delete, ctx.task_id, expected_status=204)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the trigger should have a "{prefix}" prefixed ID'))
def trigger_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.trigger is not None
    assert ctx.trigger.id.startswith(prefix), f"Expected {prefix!r}, got {ctx.trigger.id!r}"


@then(parsers.parse('the trigger name should be "{name}"'))
def trigger_name_is(ctx: ScenarioContext, name: str) -> None:
    assert ctx.trigger.name == name


@then(parsers.parse('the trigger type should be "{typ}"'))
def trigger_type_is(ctx: ScenarioContext, typ: str) -> None:
    assert ctx.trigger.type == typ


@then(parsers.parse('the trigger schedule should be "{schedule}"'))
def trigger_schedule_is(ctx: ScenarioContext, schedule: str) -> None:
    assert ctx.trigger.schedule == schedule


@then(parsers.parse('the trigger timezone should be "{tz}"'))
def trigger_timezone_is(ctx: ScenarioContext, tz: str) -> None:
    assert ctx.trigger.timezone == tz


@then(parsers.parse("the trigger enabled should be {value}"))
def trigger_enabled_is(ctx: ScenarioContext, value: str) -> None:
    expected = value.lower() == "true"
    assert ctx.trigger.enabled == expected


@then("the trigger task_id should match the parent task ID")
def trigger_task_id_matches_parent(ctx: ScenarioContext) -> None:
    expected = ctx.parent_task_id or ctx.task_id
    assert ctx.trigger.task_id == expected


@then("the trigger should have audit timestamps")
def trigger_has_audit(ctx: ScenarioContext) -> None:
    assert ctx.trigger.audit is not None
    assert ctx.trigger.audit.created_at is not None


@then("the trigger source_task_id should match the source task ID")
def trigger_source_matches(ctx: ScenarioContext) -> None:
    assert ctx.trigger.source_task_id == ctx.source_task_id


@then(parsers.parse('the trigger on_status should be "{status}"'))
def trigger_on_status_is(ctx: ScenarioContext, status: str) -> None:
    assert ctx.trigger.on_status == status


@then(parsers.parse("the trigger forward_result should be {value}"))
def trigger_forward_result_is(ctx: ScenarioContext, value: str) -> None:
    expected = value.lower() == "true"
    assert ctx.trigger.forward_result == expected


@then(parsers.parse('the trigger default_payload should contain "{key}"'))
def trigger_default_payload_contains(ctx: ScenarioContext, key: str) -> None:
    assert ctx.trigger.default_payload is not None
    assert key in ctx.trigger.default_payload


# -- Trigger list assertions ------------------------------------------------


@then('the trigger list should have an "items" array')
def trigger_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.trigger_list is not None
    assert isinstance(ctx.trigger_list, list)


@then(parsers.parse('the trigger list "items" should contain at least {n:d} triggers'))
def trigger_list_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.trigger_list) >= n


@then('the trigger list "items" should be empty')
def trigger_list_empty(ctx: ScenarioContext) -> None:
    assert len(ctx.trigger_list) == 0
