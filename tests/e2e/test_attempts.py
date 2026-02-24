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

"""Scenario wiring for attempts.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.attempt_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.run_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403

FEATURE = "../../features/attempts.feature"


@scenario(FEATURE, "List attempts for a completed run")
def test_list_attempts_for_completed_run():
    pass


@scenario(FEATURE, "Get a specific attempt by ID")
def test_get_specific_attempt():
    pass


@scenario(FEATURE, "Completed attempt has response details")
def test_completed_attempt_response_details():
    pass


@scenario(FEATURE, "List attempts with cursor pagination")
def test_list_attempts_cursor_pagination():
    pass


@scenario(FEATURE, "Get attempt for non-existent run returns 404")
def test_get_attempt_nonexistent():
    pass


@scenario(FEATURE, "Cleanup parent task")
def test_cleanup_parent_task():
    pass
