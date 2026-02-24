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

from __future__ import annotations

from pydantic import BaseModel

from switchpost.types.shared import CreatedInfo


class PolicyBinding(BaseModel):
    """A SwitchPost RBAC policy binding."""

    id: str
    tenant_id: str
    principal_id: str
    role: str
    resource_type: str
    resource_id: str
    created: CreatedInfo


class CreateBindingInputBody(BaseModel):
    """Request body for creating a policy binding."""

    role: str
    resource_type: str
    resource_id: str


__all__ = [
    "CreateBindingInputBody",
    "PolicyBinding",
]
