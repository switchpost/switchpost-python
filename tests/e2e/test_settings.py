"""Scenario wiring for settings.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.settings_steps import *  # noqa: F401, F403

FEATURE = "../../features/settings.feature"


@scenario(FEATURE, "Get tenant settings")
def test_get_tenant_settings():
    pass


@scenario(FEATURE, "Update tenant settings and verify changes")
def test_update_tenant_settings():
    pass


@scenario(FEATURE, "Update webhook allowed domains")
def test_update_webhook_allowed_domains():
    pass


@scenario(FEATURE, "Update default result TTL")
def test_update_default_result_ttl():
    pass


@scenario(FEATURE, "Settings round-trip preserves all fields")
def test_settings_round_trip():
    pass
