"""Scenario wiring for triggers.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.trigger_steps import *  # noqa: F401, F403

FEATURE = "../../features/triggers.feature"


@scenario(FEATURE, "Full CRON trigger CRUD lifecycle")
def test_full_cron_trigger_crud_lifecycle():
    pass


@scenario(FEATURE, "Create an HTTP trigger")
def test_create_http_trigger():
    pass


@scenario(FEATURE, "Create an EVENT trigger with source task")
def test_create_event_trigger_with_source_task():
    pass


@scenario(FEATURE, "Create a CRON trigger with default payload")
def test_create_cron_trigger_with_default_payload():
    pass


@scenario(FEATURE, "Create a disabled trigger")
def test_create_disabled_trigger():
    pass


@scenario(FEATURE, "Update trigger enabled state")
def test_update_trigger_enabled_state():
    pass


@scenario(FEATURE, "List triggers for a task")
def test_list_triggers_for_task():
    pass


@scenario(FEATURE, "List triggers for a task with no triggers returns empty list")
def test_list_triggers_empty():
    pass


@scenario(FEATURE, "Cleanup parent task")
def test_cleanup_parent_task():
    pass
