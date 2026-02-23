"""Scenario wiring for principals.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.principal_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403

FEATURE = "../../features/principals.feature"


@scenario(FEATURE, "Full API key principal CRUD lifecycle")
def test_full_api_key_principal_crud():
    pass


@scenario(FEATURE, "Create an API key principal with expiration")
def test_create_api_key_with_expiration():
    pass


@scenario(FEATURE, "Create a user principal")
def test_create_user_principal():
    pass


@scenario(FEATURE, "List principals with offset pagination")
def test_list_principals_offset_pagination():
    pass


@scenario(FEATURE, "List principals with default pagination")
def test_list_principals_default_pagination():
    pass


@scenario(FEATURE, "Get non-existent principal returns 404")
def test_get_nonexistent_principal():
    pass


@scenario(FEATURE, "Delete non-existent principal returns 404")
def test_delete_nonexistent_principal():
    pass


@scenario(FEATURE, "Created API key can authenticate")
def test_created_api_key_authenticates():
    pass
