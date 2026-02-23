"""Scenario wiring for errors.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.binding_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.principal_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.run_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.trigger_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.webhook_steps import *  # noqa: F401, F403

FEATURE = "../../features/errors.feature"


@scenario(FEATURE, "Request with no credentials returns 401")
def test_request_no_credentials():
    pass


@scenario(FEATURE, "Request with invalid API key returns 401")
def test_request_invalid_api_key():
    pass


@scenario(FEATURE, "Get non-existent task returns 404")
def test_get_nonexistent_task():
    pass


@scenario(FEATURE, "Get non-existent run returns 404")
def test_get_nonexistent_run():
    pass


@scenario(FEATURE, "Get non-existent principal returns 404")
def test_get_nonexistent_principal():
    pass


@scenario(FEATURE, "Delete non-existent task returns 404")
def test_delete_nonexistent_task():
    pass


@scenario(FEATURE, "Get trigger on non-existent task returns 404")
def test_get_trigger_nonexistent_task():
    pass


@scenario(FEATURE, "Get attempt on non-existent run returns 404")
def test_get_attempt_nonexistent_run():
    pass


@scenario(FEATURE, "Create task without required name field returns 422")
def test_create_task_missing_name():
    pass


@scenario(FEATURE, "Create task without required endpoint_url field returns 422")
def test_create_task_missing_endpoint_url():
    pass


@scenario(FEATURE, "Create task with invalid name format returns 422")
def test_create_task_invalid_name():
    pass


@scenario(FEATURE, "Create trigger without required type field returns 422")
def test_create_trigger_missing_type():
    pass


@scenario(FEATURE, "Create CRON trigger without schedule returns 422")
def test_create_cron_trigger_missing_schedule():
    pass


@scenario(FEATURE, "Create principal without required type field returns 422")
def test_create_principal_missing_type():
    pass


@scenario(FEATURE, "Create binding without required fields returns 422")
def test_create_binding_missing_fields():
    pass


@scenario(FEATURE, "Create webhook without required url field returns 422")
def test_create_webhook_missing_url():
    pass


@scenario(FEATURE, "Create task with duplicate name returns 409")
def test_create_task_duplicate_name():
    pass


@scenario(FEATURE, "Error responses follow RFC 7807 structure")
def test_error_rfc7807_structure():
    pass
