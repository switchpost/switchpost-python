"""Scenario wiring for bindings.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.binding_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.principal_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403

FEATURE = "../../features/bindings.feature"


@scenario(FEATURE, "Create, list, and delete a tenant-scoped binding")
def test_create_list_delete_tenant_binding():
    pass


@scenario(FEATURE, "Create a task-scoped binding")
def test_create_task_scoped_binding():
    pass


@scenario(FEATURE, "Create multiple bindings for one principal")
def test_create_multiple_bindings():
    pass


@scenario(FEATURE, "Delete a non-existent binding returns 404")
def test_delete_nonexistent_binding():
    pass


@scenario(FEATURE, "List bindings for a principal with no bindings returns empty list")
def test_list_bindings_empty():
    pass


@scenario(FEATURE, "Binding survives principal read (consistency check)")
def test_binding_survives_principal_read():
    pass


@scenario(FEATURE, "Cleanup principal")
def test_cleanup_principal():
    pass
