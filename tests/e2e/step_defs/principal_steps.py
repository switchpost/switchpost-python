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

"""Step definitions for Principal management (principals.feature)."""

from __future__ import annotations

import contextlib

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError, SwitchPost

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I create a principal with the following properties:")
def create_principal(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    # If required fields are missing, use raw HTTP call for API validation
    if "type" not in kwargs or "name" not in kwargs:
        resp = safe_call(
            ctx,
            lambda: _raw_create_principal(ctx.client, kwargs),
            expected_status=201,
        )
    else:
        resp = safe_call(ctx, ctx.client.principals.create, expected_status=201, **kwargs)

    if resp is not None:
        ctx.principal_response = resp
        ctx.principal = resp.principal
        ctx.principal_id = resp.principal.id
        ctx.created_principals.append(resp.principal.id)


def _raw_create_principal(client, body: dict):
    """Raw POST for principal creation when required fields may be missing."""
    from switchpost.types.principal import CreatePrincipalResponse

    response = client._request("POST", "/principals", json=body)
    return CreatePrincipalResponse.model_validate(response.json())


@when("I get the principal by its ID")
def get_principal_by_id(ctx: ScenarioContext) -> None:
    principal = safe_call(ctx, ctx.client.principals.get, ctx.principal_id, expected_status=200)
    if principal is not None:
        ctx.principal = principal


@when(parsers.parse('I get a principal with ID "{principal_id}"'))
def get_principal_explicit(ctx: ScenarioContext, principal_id: str) -> None:
    safe_call(ctx, ctx.client.principals.get, principal_id, expected_status=200)


@when("I delete the principal")
def delete_principal(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.principals.delete, ctx.principal_id, expected_status=204)


@when(parsers.parse('I delete a principal with ID "{principal_id}"'))
def delete_principal_explicit(ctx: ScenarioContext, principal_id: str) -> None:
    safe_call(ctx, ctx.client.principals.delete, principal_id, expected_status=204)


@when("I delete the principal using the original client")
def delete_principal_original_client(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.principals.delete, ctx.principal_id, expected_status=204)


@when("I list principals")
def list_principals_default(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.principals.list, expected_status=200)
    if result is not None:
        ctx.principal_list = result


@when(parsers.parse("I list principals with limit {limit:d} and offset {offset:d}"))
def list_principals_with_params(ctx: ScenarioContext, limit: int, offset: int) -> None:
    result = safe_call(ctx, ctx.client.principals.list, offset=offset, limit=limit, expected_status=200)
    if result is not None:
        ctx.principal_list = result


@when(parsers.parse('I delete all principals with name prefix "{prefix}"'))
def delete_principals_by_prefix(ctx: ScenarioContext, prefix: str) -> None:
    page = ctx.client.principals.list(limit=200)
    for prn in page.data:
        if prn.name.startswith(prefix):
            with contextlib.suppress(APIError):
                ctx.client.principals.delete(prn.id)


@when("I create a new client using the returned API key")
def create_new_client_from_api_key(ctx: ScenarioContext) -> None:
    api_key = ctx.principal_response.api_key
    base_url = ctx.client._config.base_url
    ctx.new_client = SwitchPost(base_url=base_url, api_key=api_key)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then('the response should include a "principal" object')
def response_has_principal(ctx: ScenarioContext) -> None:
    assert ctx.principal_response is not None
    assert ctx.principal_response.principal is not None


@then(parsers.parse('the principal should have a "{prefix}" prefixed ID'))
def principal_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.principal.id.startswith(prefix), f"Expected {prefix!r}, got {ctx.principal.id!r}"


@then(parsers.parse('the principal name should be "{name}"'))
def principal_name_is(ctx: ScenarioContext, name: str) -> None:
    assert ctx.principal.name == name


@then(parsers.parse('the principal type should be "{typ}"'))
def principal_type_is(ctx: ScenarioContext, typ: str) -> None:
    assert ctx.principal.type == typ


@then("the principal should have audit timestamps")
def principal_has_audit(ctx: ScenarioContext) -> None:
    assert ctx.principal.audit is not None
    assert ctx.principal.audit.created_at is not None


@then('the response should include an "api_key" string')
def response_has_api_key(ctx: ScenarioContext) -> None:
    assert ctx.principal_response is not None
    assert isinstance(ctx.principal_response.api_key, str)
    assert len(ctx.principal_response.api_key) > 0


@then("the principal should have a key_prefix")
def principal_has_key_prefix(ctx: ScenarioContext) -> None:
    assert ctx.principal.key_prefix is not None
    assert len(ctx.principal.key_prefix) > 0


@then("the principal expires_at should be present")
def principal_expires_at_present(ctx: ScenarioContext) -> None:
    assert ctx.principal.expires_at is not None


@then(parsers.parse('the principal email should be "{email}"'))
def principal_email_is(ctx: ScenarioContext, email: str) -> None:
    assert ctx.principal.email == email


# -- Principal list assertions -----------------------------------------------


@then('the principal list should have an "items" array')
def principal_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.principal_list is not None
    assert isinstance(ctx.principal_list.data, list)


@then(parsers.parse('the principal list should have a "total" count of at least {n:d}'))
def principal_list_total_at_least(ctx: ScenarioContext, n: int) -> None:
    assert ctx.principal_list.pagination.total >= n


@then('the principal list should have a "total" count')
def principal_list_has_total(ctx: ScenarioContext) -> None:
    assert ctx.principal_list.pagination.total is not None


@then('the principal list should have an "offset" value')
def principal_list_has_offset(ctx: ScenarioContext) -> None:
    assert ctx.principal_list.pagination.offset is not None


@then('the principal list should have a "limit" value')
def principal_list_has_limit(ctx: ScenarioContext) -> None:
    assert ctx.principal_list.pagination.limit is not None


@then(parsers.parse('the principal list "limit" should be {value:d}'))
def principal_list_limit_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.principal_list.pagination.limit == value


@then(parsers.parse('the principal list "offset" should be {value:d}'))
def principal_list_offset_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.principal_list.pagination.offset == value


@then(parsers.parse('the principal list "items" should contain at most {n:d} principals'))
def principal_list_items_at_most(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.principal_list.data) <= n


@then(parsers.parse('the principal list "items" should contain at least {n:d} principal'))
def principal_list_items_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.principal_list.data) >= n
