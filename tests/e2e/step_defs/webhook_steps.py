"""Step definitions for Webhook management (webhooks.feature)."""

from __future__ import annotations

import contextlib

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

from switchpost import APIError

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I create a webhook on the run with the following properties:")
def create_webhook(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    # If required 'url' is missing, use raw HTTP call for API validation
    if "url" not in kwargs:
        webhook = safe_call(
            ctx,
            lambda: _raw_create_webhook(ctx.client, ctx.run_id, kwargs),
            expected_status=201,
        )
    else:
        webhook = safe_call(
            ctx,
            ctx.client.webhooks.create,
            ctx.run_id,
            expected_status=201,
            **kwargs,
        )

    if webhook is not None:
        ctx.webhook = webhook
        ctx.webhook_id = webhook.id
        ctx.created_webhooks.append((ctx.run_id, webhook.id))


def _raw_create_webhook(client, run_id: str, body: dict):
    """Raw POST for webhook creation when required fields may be missing."""
    from switchpost.types.webhook import Webhook

    response = client._request("POST", f"/runs/{run_id}/webhooks", json=body)
    return Webhook.model_validate(response.json())


@when("I list webhooks for the run")
def list_webhooks(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.webhooks.list, ctx.run_id, expected_status=200)
    if result is not None:
        ctx.webhook_list = result


@when("I list webhooks for the new run")
def list_webhooks_new_run(ctx: ScenarioContext) -> None:
    result = safe_call(ctx, ctx.client.webhooks.list, ctx.another_run_id, expected_status=200)
    if result is not None:
        ctx.webhook_list = result


@when("I delete the webhook")
def delete_webhook(ctx: ScenarioContext) -> None:
    safe_call(ctx, ctx.client.webhooks.delete, ctx.run_id, ctx.webhook_id, expected_status=204)


@when(parsers.parse('I delete a webhook with ID "{webhook_id}" on the run'))
def delete_webhook_explicit(ctx: ScenarioContext, webhook_id: str) -> None:
    safe_call(ctx, ctx.client.webhooks.delete, ctx.run_id, webhook_id, expected_status=204)


@when("I delete all webhooks for the run")
def delete_all_webhooks(ctx: ScenarioContext) -> None:
    webhooks = ctx.client.webhooks.list(ctx.run_id)
    for wh in webhooks:
        with contextlib.suppress(APIError):
            ctx.client.webhooks.delete(ctx.run_id, wh.id)


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the webhook should have a "{prefix}" prefixed ID'))
def webhook_has_prefixed_id(ctx: ScenarioContext, prefix: str) -> None:
    assert ctx.webhook is not None
    assert ctx.webhook.id.startswith(prefix), f"Expected {prefix!r}, got {ctx.webhook.id!r}"


@then(parsers.parse('the webhook url should be "{url}"'))
def webhook_url_is(ctx: ScenarioContext, url: str) -> None:
    assert ctx.webhook.url == url


@then("the webhook run_id should match the run ID")
def webhook_run_id_matches(ctx: ScenarioContext) -> None:
    assert ctx.webhook.run_id == ctx.run_id


@then("the webhook should have created info with created_at and created_by")
def webhook_has_created_info(ctx: ScenarioContext) -> None:
    assert ctx.webhook.created is not None
    assert ctx.webhook.created.created_at is not None
    assert ctx.webhook.created.created_by is not None


# -- Webhook list assertions ------------------------------------------------


@then('the webhook list should have an "items" array')
def webhook_list_has_items(ctx: ScenarioContext) -> None:
    assert ctx.webhook_list is not None
    assert isinstance(ctx.webhook_list, list)


@then(parsers.parse('the webhook list "items" should contain at least {n:d} webhook'))
def webhook_list_at_least(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.webhook_list) >= n


@then(parsers.parse('the webhook list "items" should contain at least {n:d} webhooks'))
def webhook_list_at_least_plural(ctx: ScenarioContext, n: int) -> None:
    assert len(ctx.webhook_list) >= n


@then("the webhook list should contain the created webhook")
def webhook_list_contains_created(ctx: ScenarioContext) -> None:
    ids = [wh.id for wh in ctx.webhook_list]
    assert ctx.webhook_id in ids


@then('the webhook list "items" should not contain the deleted webhook')
def webhook_list_not_contains_deleted(ctx: ScenarioContext) -> None:
    ids = [wh.id for wh in ctx.webhook_list]
    assert ctx.webhook_id not in ids


@then('the webhook list "items" should be empty')
def webhook_list_empty(ctx: ScenarioContext) -> None:
    assert len(ctx.webhook_list) == 0
