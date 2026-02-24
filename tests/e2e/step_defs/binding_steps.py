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

"""Step definitions for Policy Binding management (bindings.feature)."""

from __future__ import annotations

import contextlib

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I create a binding for the principal with the following properties:")
def create_binding(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        if key == "resource_id" and raw_val == "<task_id>":
            kwargs[key] = ctx.task_id
        else:
            kwargs[key] = parse_typed_value(raw_val)

    # If required fields are missing, use raw HTTP call for API validation
    required = {"role", "resource_type", "resource_id"}
    if not required.issubset(kwargs.keys()):
        binding = safe_call(
            ctx,
            lambda: _raw_create_binding(ctx.client, ctx.principal_id, kwargs),
            expected_status=201,
        )
    else:
        binding = safe_call(
            ctx,
            ctx.client.bindings.create,
            ctx.principal_id,
            expected_status=201,
            **kwargs,
        )

    if binding is not None:
        ctx.binding = binding
        ctx.binding_id = binding.id
        ctx.created_bindings.append(binding.id)


def _raw_create_binding(client, principal_id: str, body: dict):
    """Raw POST for binding creation when required fields may be missing."""
    from switchpost.types.binding import PolicyBinding

    response = client._request("POST", f"/principals/{principal_id}/bindings", json=body)
    return PolicyBinding.model_validate(response.json())


@when("I list bindings for the principal")
def list_bindings(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.bindings.list, ctx.principal_id, expected_status=200)
    if result is not None:
        ctx.binding_list = result


@when("I list bindings for the new principal")
def list_bindings_new_principal(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.bindings.list, ctx.another_principal_id, expected_status=200)
    if result is not None:
        ctx.binding_list = result


@when("I delete the binding by its ID")
def delete_binding(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.bindings.delete, ctx.binding_id, expected_status=204)


@when(parsers.parse('I delete a binding with ID "{binding_id}"'))
def delete_binding_explicit(ctx: ScenarioContext, binding_id: str) -> None:
    safe_call(ctx, ctx.client.bindings.delete, binding_id, expected_status=204)


@when("I delete all bindings for the principal")
def delete_all_bindings(ctx: ScenarioContext) -> None:
    bindings = ctx.client.bindings.list(ctx.principal_id)
    for b in bindings:
        with contextlib.suppress(APIError):
            ctx.client.bindings.delete(b.id)


@when("I delete the new principal")
def delete_new_principal(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.principals.delete, ctx.another_principal_id, expected_status=204)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the binding should have a "{prefix}" prefixed ID'))
def binding_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.binding is not None
    assert ctx.binding.id.startswith(prefix), f"Expected {prefix!r}, got {ctx.binding.id!r}"


@then(parsers.parse('the binding role should be "{role}"'))
def binding_role_is(ctx: ScenarioContext, role: str) -> None:
    assert ctx.binding.role == role


@then(parsers.parse('the binding resource_type should be "{rt}"'))
def binding_resource_type_is(ctx: ScenarioContext, rt: str) -> None:
    assert ctx.binding.resource_type == rt


@then(parsers.parse('the binding resource_id should be "{rid}"'))
def binding_resource_id_is(ctx: ScenarioContext, rid: str) -> None:
    assert ctx.binding.resource_id == rid


@then("the binding resource_id should match the task ID")
def binding_resource_id_matches_task(ctx: ScenarioContext) -> None:
    assert ctx.binding.resource_id == ctx.task_id


@then("the binding principal_id should match the principal ID")
def binding_principal_id_matches(ctx: ScenarioContext) -> None:
    assert ctx.binding.principal_id == ctx.principal_id


@then("the binding should have created info with created_at and created_by")
def binding_has_created_info(ctx: ScenarioContext) -> None:
    assert ctx.binding.created is not None
    assert ctx.binding.created.created_at is not None
    assert ctx.binding.created.created_by is not None


# -- Binding list assertions -------------------------------------------------


@then('the binding list should have an "items" array')
def binding_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.binding_list is not None
    assert isinstance(ctx.binding_list, list)


@then(parsers.parse('the binding list "items" should contain at least {n:d} binding'))
def binding_list_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.binding_list) >= n


@then(parsers.parse('the binding list "items" should contain at least {n:d} bindings'))
def binding_list_at_least_plural(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.binding_list) >= n


@then("the binding list should contain the created binding")
def binding_list_contains_created(ctx: ScenarioContext) -> None:
    ids = [b.id for b in ctx.binding_list]
    assert ctx.binding_id in ids


@then('the binding list "items" should not contain the deleted binding')
def binding_list_not_contains_deleted(ctx: ScenarioContext) -> None:
    ids = [b.id for b in ctx.binding_list]
    assert ctx.binding_id not in ids


@then('the binding list "items" should be empty')
def binding_list_empty(ctx: ScenarioContext) -> None:
    assert len(ctx.binding_list) == 0
