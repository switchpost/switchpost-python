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

"""Scenario wiring for webhooks.feature."""

from pytest_bdd import scenario
from tests.e2e.step_defs.common_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.given_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.task_steps import *  # noqa: F401, F403
from tests.e2e.step_defs.webhook_steps import *  # noqa: F401, F403

FEATURE = "../../features/webhooks.feature"


@scenario(FEATURE, "Create, list, and delete a webhook")
def test_create_list_delete_webhook():
    pass


@scenario(FEATURE, "Create a webhook with HMAC secret")
def test_create_webhook_with_hmac_secret():
    pass


@scenario(FEATURE, "Create multiple webhooks on the same run")
def test_create_multiple_webhooks():
    pass


@scenario(FEATURE, "List webhooks for a run with no webhooks returns empty list")
def test_list_webhooks_empty():
    pass


@scenario(FEATURE, "Delete a non-existent webhook returns 404")
def test_delete_nonexistent_webhook():
    pass


@scenario(FEATURE, "Cleanup parent task")
def test_cleanup_parent_task():
    pass
