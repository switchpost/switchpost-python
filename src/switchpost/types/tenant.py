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

from switchpost.types.shared import AuditInfo


class Tenant(BaseModel):
    """A SwitchPost tenant."""

    id: str
    name: str
    display_name: str
    audit: AuditInfo


class CreateTenantInputBody(BaseModel):
    """Request body for creating a tenant (admin only)."""

    name: str
    display_name: str


class CreateTenantResponse(BaseModel):
    """Response body when creating a tenant (includes initial API key and principal ID)."""

    tenant: Tenant
    api_key: str
    principal_id: str


__all__ = [
    "CreateTenantInputBody",
    "CreateTenantResponse",
    "Tenant",
]
