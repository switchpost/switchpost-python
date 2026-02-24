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

from switchpost._client import AsyncSwitchPost, SwitchPost
from switchpost._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ConnectionError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    SwitchPostError,
    UnprocessableEntityError,
)
from switchpost._version import __version__
from switchpost.types import (
    AuditInfo,
    CreateBindingInputBody,
    CreatedInfo,
    CreatePrincipalInputBody,
    CreatePrincipalResponse,
    CreateTaskInputBody,
    CreateTenantInputBody,
    CreateTenantResponse,
    CreateTriggerInputBody,
    CreateWebhookInputBody,
    CursorPaginationMeta,
    ErrorDetail,
    ErrorModel,
    OffsetPaginationMeta,
    PolicyBinding,
    Principal,
    RateLimit,
    RetryPolicy,
    SubmitRunInputBody,
    SystemSettings,
    Task,
    TaskResultMeta,
    TaskRun,
    TaskRunAttempt,
    Tenant,
    TenantSettings,
    Trigger,
    UpdateTaskInputBody,
    UpdateTriggerInputBody,
    Webhook,
)

__all__ = [
    # Clients
    "AsyncSwitchPost",
    "SwitchPost",
    # Version
    "__version__",
    # Errors
    "APIError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "ConnectionError",
    "InternalServerError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "SwitchPostError",
    "UnprocessableEntityError",
    # Types
    "AuditInfo",
    "CreateBindingInputBody",
    "CreatePrincipalInputBody",
    "CreatePrincipalResponse",
    "CreateTaskInputBody",
    "CreateTenantInputBody",
    "CreateTenantResponse",
    "CreateTriggerInputBody",
    "CreateWebhookInputBody",
    "CreatedInfo",
    "CursorPaginationMeta",
    "ErrorDetail",
    "ErrorModel",
    "OffsetPaginationMeta",
    "PolicyBinding",
    "Principal",
    "RateLimit",
    "RetryPolicy",
    "SubmitRunInputBody",
    "SystemSettings",
    "Task",
    "TaskResultMeta",
    "TaskRun",
    "TaskRunAttempt",
    "Tenant",
    "TenantSettings",
    "Trigger",
    "UpdateTaskInputBody",
    "UpdateTriggerInputBody",
    "Webhook",
]
