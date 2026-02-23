from __future__ import annotations

from pydantic import BaseModel

from switchpost.types.shared import CreatedInfo


class Webhook(BaseModel):
    """A SwitchPost webhook subscription on a run."""

    id: str
    run_id: str
    url: str
    created: CreatedInfo
    secret_ref: str | None = None


class CreateWebhookInputBody(BaseModel):
    """Request body for registering a webhook on a run."""

    url: str
    secret: str | None = None


__all__ = [
    "CreateWebhookInputBody",
    "Webhook",
]
