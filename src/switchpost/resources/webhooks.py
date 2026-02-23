from typing import TYPE_CHECKING, Any

from switchpost.types.webhook import Webhook

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class WebhooksResource:
    """Synchronous webhooks API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(self, run_id: str) -> list[Webhook]:
        """List webhooks for a run.

        Args:
            run_id: Run ID.

        Returns:
            A list of webhooks. Webhooks use a simple list (not paginated).
        """
        response = self._client._request("GET", f"/runs/{run_id}/webhooks")
        body = response.json()
        return [Webhook.model_validate(item) for item in (body.get("items") or [])]

    def create(
        self,
        run_id: str,
        *,
        url: str,
        secret: str | None = None,
    ) -> Webhook:
        """Register a webhook for a run.

        Args:
            run_id: Run ID.
            url: HTTPS endpoint URL for webhook delivery, max 2048 chars.
            secret: Optional HMAC secret for webhook payload signing.
        """
        body = _create_body(url=url, secret=secret)
        response = self._client._request("POST", f"/runs/{run_id}/webhooks", json=body)
        return Webhook.model_validate(response.json())

    def delete(self, run_id: str, webhook_id: str) -> None:
        """Delete a webhook.

        Args:
            run_id: Run ID.
            webhook_id: Webhook ID.
        """
        self._client._request("DELETE", f"/runs/{run_id}/webhooks/{webhook_id}")


class AsyncWebhooksResource:
    """Asynchronous webhooks API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(self, run_id: str) -> list[Webhook]:
        """List webhooks for a run.

        Args:
            run_id: Run ID.

        Returns:
            A list of webhooks. Webhooks use a simple list (not paginated).
        """
        response = await self._client._request("GET", f"/runs/{run_id}/webhooks")
        body = response.json()
        return [Webhook.model_validate(item) for item in (body.get("items") or [])]

    async def create(
        self,
        run_id: str,
        *,
        url: str,
        secret: str | None = None,
    ) -> Webhook:
        """Register a webhook for a run.

        Args:
            run_id: Run ID.
            url: HTTPS endpoint URL for webhook delivery, max 2048 chars.
            secret: Optional HMAC secret for webhook payload signing.
        """
        body = _create_body(url=url, secret=secret)
        response = await self._client._request("POST", f"/runs/{run_id}/webhooks", json=body)
        return Webhook.model_validate(response.json())

    async def delete(self, run_id: str, webhook_id: str) -> None:
        """Delete a webhook.

        Args:
            run_id: Run ID.
            webhook_id: Webhook ID.
        """
        await self._client._request("DELETE", f"/runs/{run_id}/webhooks/{webhook_id}")


# --- Private helpers ---


def _create_body(*, url: str, secret: str | None) -> dict[str, Any]:
    body: dict[str, Any] = {"url": url}
    if secret is not None:
        body["secret"] = secret
    return body
