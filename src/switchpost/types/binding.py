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
