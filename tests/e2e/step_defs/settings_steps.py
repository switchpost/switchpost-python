"""Step definitions for Tenant Settings management (settings.feature)."""

from __future__ import annotations

from pytest_bdd import parsers, then, when
from tests.e2e.conftest import ScenarioContext, parse_table, parse_typed_value, safe_call

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("I get the tenant settings")
def get_settings(ctx: ScenarioContext) -> None:
    settings = safe_call(ctx, ctx.client.settings.get, expected_status=200)
    if settings is not None:
        ctx.settings = settings


@when("I update the tenant settings with the following properties:")
def update_settings(ctx: ScenarioContext, datatable) -> None:
    props = parse_table(datatable)
    kwargs: dict = {}
    for key, raw_val in props.items():
        kwargs[key] = parse_typed_value(raw_val)

    settings = safe_call(ctx, ctx.client.settings.update, expected_status=200, **kwargs)
    if settings is not None:
        ctx.settings = settings


@when("I restore the original tenant settings")
def restore_settings(ctx: ScenarioContext) -> None:
    assert ctx.saved_settings is not None, "No saved settings to restore"
    s = ctx.saved_settings
    settings = safe_call(
        ctx,
        ctx.client.settings.update,
        expected_status=200,
        default_max_attempts=s.default_max_attempts,
        default_initial_delay_ms=s.default_initial_delay_ms,
        webhook_allowed_domains=s.webhook_allowed_domains,
        oauth_auto_provisioning=s.oauth_auto_provisioning,
        api_rate_limit_per_minute=s.api_rate_limit_per_minute,
        api_rate_limit_burst_size=s.api_rate_limit_burst_size,
        max_batch_size=s.max_batch_size,
        default_priority=s.default_priority,
        default_result_ttl_seconds=s.default_result_ttl_seconds,
    )
    if settings is not None:
        ctx.settings = settings


@when("I update the tenant settings with the saved settings")
def update_with_saved(ctx: ScenarioContext) -> None:
    assert ctx.saved_settings is not None
    s = ctx.saved_settings
    settings = safe_call(
        ctx,
        ctx.client.settings.update,
        expected_status=200,
        default_max_attempts=s.default_max_attempts,
        default_initial_delay_ms=s.default_initial_delay_ms,
        webhook_allowed_domains=s.webhook_allowed_domains,
        oauth_auto_provisioning=s.oauth_auto_provisioning,
        api_rate_limit_per_minute=s.api_rate_limit_per_minute,
        api_rate_limit_burst_size=s.api_rate_limit_burst_size,
        max_batch_size=s.max_batch_size,
        default_priority=s.default_priority,
        default_result_ttl_seconds=s.default_result_ttl_seconds,
    )
    if settings is not None:
        ctx.settings = settings


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("I save the current settings")
def save_current_settings(ctx: ScenarioContext) -> None:
    assert ctx.settings is not None
    ctx.saved_settings = ctx.settings


@then(parsers.parse('the settings should have a "{field}" integer'))
def settings_has_integer(ctx: ScenarioContext, field: str) -> None:
    value = getattr(ctx.settings, field, None)
    assert value is not None, f"settings.{field} is None"
    assert isinstance(value, int), f"settings.{field} is {type(value)}, not int"


@then(parsers.parse('the settings should have a "{field}" value'))
def settings_has_value(ctx: ScenarioContext, field: str) -> None:
    # webhook_allowed_domains may be None or a list -- just check field exists
    assert hasattr(ctx.settings, field), f"settings has no attribute {field!r}"


@then(parsers.parse('the settings should have an "{field}" boolean'))
def settings_has_boolean(ctx: ScenarioContext, field: str) -> None:
    value = getattr(ctx.settings, field, None)
    assert isinstance(value, bool), f"settings.{field} is {type(value)}, not bool"


@then(parsers.parse('the settings should have an "{field}" integer'))
def settings_has_integer_an(ctx: ScenarioContext, field: str) -> None:
    value = getattr(ctx.settings, field, None)
    assert value is not None, f"settings.{field} is None"
    assert isinstance(value, int), f"settings.{field} is {type(value)}, not int"


@then(parsers.parse("the settings default_max_attempts should be {value:d}"))
def settings_max_attempts_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.default_max_attempts == value


@then(parsers.parse("the settings default_initial_delay_ms should be {value:d}"))
def settings_initial_delay_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.default_initial_delay_ms == value


@then(parsers.parse("the settings api_rate_limit_per_minute should be {value:d}"))
def settings_rate_limit_per_minute_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.api_rate_limit_per_minute == value


@then(parsers.parse("the settings api_rate_limit_burst_size should be {value:d}"))
def settings_rate_limit_burst_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.api_rate_limit_burst_size == value


@then(parsers.parse("the settings max_batch_size should be {value:d}"))
def settings_max_batch_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.max_batch_size == value


@then(parsers.parse("the settings default_priority should be {value:d}"))
def settings_default_priority_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.default_priority == value


@then(parsers.parse("the settings oauth_auto_provisioning should be {value}"))
def settings_oauth_auto_prov_is(ctx: ScenarioContext, value: str) -> None:
    expected = value.lower() == "true"
    assert ctx.settings.oauth_auto_provisioning == expected


@then(parsers.parse("the settings default_result_ttl_seconds should be {value:d}"))
def settings_result_ttl_is(ctx: ScenarioContext, value: int) -> None:
    assert ctx.settings.default_result_ttl_seconds == value


@then(parsers.parse('the settings webhook_allowed_domains should contain "{domain}"'))
def settings_webhook_domains_contains(ctx: ScenarioContext, domain: str) -> None:
    assert ctx.settings.webhook_allowed_domains is not None
    assert domain in ctx.settings.webhook_allowed_domains


@then("the settings should match the saved settings")
def settings_match_saved(ctx: ScenarioContext) -> None:
    s = ctx.saved_settings
    c = ctx.settings
    assert c.default_max_attempts == s.default_max_attempts
    assert c.default_initial_delay_ms == s.default_initial_delay_ms
    assert c.oauth_auto_provisioning == s.oauth_auto_provisioning
    assert c.api_rate_limit_per_minute == s.api_rate_limit_per_minute
    assert c.api_rate_limit_burst_size == s.api_rate_limit_burst_size
    assert c.max_batch_size == s.max_batch_size
    assert c.default_priority == s.default_priority
    assert c.webhook_allowed_domains == s.webhook_allowed_domains
    assert c.default_result_ttl_seconds == s.default_result_ttl_seconds
