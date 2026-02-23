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
