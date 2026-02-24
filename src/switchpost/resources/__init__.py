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

from switchpost.resources.admin import AdminResource, AsyncAdminResource
from switchpost.resources.attempts import AsyncAttemptsResource, AttemptsResource
from switchpost.resources.bindings import AsyncBindingsResource, BindingsResource
from switchpost.resources.principals import AsyncPrincipalsResource, PrincipalsResource
from switchpost.resources.runs import AsyncRunsResource, RunsResource
from switchpost.resources.settings import AsyncSettingsResource, SettingsResource
from switchpost.resources.tasks import AsyncTasksResource, TasksResource
from switchpost.resources.triggers import AsyncTriggersResource, TriggersResource
from switchpost.resources.webhooks import AsyncWebhooksResource, WebhooksResource

__all__ = [
    "AdminResource",
    "AsyncAdminResource",
    "AsyncAttemptsResource",
    "AsyncBindingsResource",
    "AsyncPrincipalsResource",
    "AsyncRunsResource",
    "AsyncSettingsResource",
    "AsyncTasksResource",
    "AsyncTriggersResource",
    "AsyncWebhooksResource",
    "AttemptsResource",
    "BindingsResource",
    "PrincipalsResource",
    "RunsResource",
    "SettingsResource",
    "TasksResource",
    "TriggersResource",
    "WebhooksResource",
]
