from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from switchpost.types.shared import AuditInfo


class Principal(BaseModel):
    """A SwitchPost principal (user or API key)."""

    id: str
    type: str
    name: str
    audit: AuditInfo
    email: str | None = None
    oauth_provider: str | None = None
    oauth_subject: str | None = None
    key_prefix: str | None = None
    expires_at: datetime | None = None
    last_seen_at: datetime | None = None


class CreatePrincipalInputBody(BaseModel):
    """Request body for creating a principal."""

    type: str
    name: str
    email: str | None = None
    oauth_provider: str | None = None
    oauth_subject: str | None = None
    expires_at: datetime | None = None


class CreatePrincipalResponse(BaseModel):
    """Response body when creating a principal (includes raw API key)."""

    principal: Principal
    api_key: str | None = None


__all__ = [
    "CreatePrincipalInputBody",
    "CreatePrincipalResponse",
    "Principal",
]
