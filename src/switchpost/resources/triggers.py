from typing import TYPE_CHECKING, Any

from switchpost.types.trigger import Trigger

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class TriggersResource:
    """Synchronous triggers API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(self, task_id: str) -> list[Trigger]:
        """List triggers for a task.

        Args:
            task_id: Parent task ID.

        Returns:
            A list of triggers. Triggers use a simple list (not paginated).
        """
        response = self._client._request("GET", f"/tasks/{task_id}/triggers")
        body = response.json()
        return [Trigger.model_validate(item) for item in (body.get("items") or [])]

    def get(self, task_id: str, trigger_id: str) -> Trigger:
        """Get a trigger by ID.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
        """
        response = self._client._request("GET", f"/tasks/{task_id}/triggers/{trigger_id}")
        return Trigger.model_validate(response.json())

    def create(
        self,
        task_id: str,
        *,
        name: str,
        type: str,
        schedule: str | None = None,
        timezone: str | None = None,
        source_task_id: str | None = None,
        on_status: str | None = None,
        forward_result: bool | None = None,
        default_payload: Any | None = None,
        enabled: bool | None = None,
    ) -> Trigger:
        """Create a new trigger for a task.

        Args:
            task_id: Parent task ID.
            name: Human-readable trigger label.
            type: Trigger mechanism: HTTP, CRON, EVENT, or QUEUE.
            schedule: Cron expression (required for CRON type).
            timezone: IANA timezone for CRON schedule.
            source_task_id: Source task ID (required for EVENT type).
            on_status: Terminal status filter for EVENT type.
            forward_result: Forward source result as payload for EVENT type.
            default_payload: Optional default JSON payload.
            enabled: Whether the trigger is active. Default: true.
        """
        body = _create_body(
            name=name,
            type=type,
            schedule=schedule,
            timezone=timezone,
            source_task_id=source_task_id,
            on_status=on_status,
            forward_result=forward_result,
            default_payload=default_payload,
            enabled=enabled,
        )
        response = self._client._request("POST", f"/tasks/{task_id}/triggers", json=body)
        return Trigger.model_validate(response.json())

    def update(
        self,
        task_id: str,
        trigger_id: str,
        *,
        name: str | None = None,
        schedule: str | None = None,
        timezone: str | None = None,
        source_task_id: str | None = None,
        on_status: str | None = None,
        forward_result: bool | None = None,
        default_payload: Any | None = None,
        enabled: bool | None = None,
    ) -> Trigger:
        """Partially update a trigger. Only provided fields are changed.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
            name: Updated trigger label.
            schedule: Updated cron expression.
            timezone: Updated IANA timezone.
            source_task_id: Updated source task ID.
            on_status: Updated terminal status filter.
            forward_result: Updated result forwarding flag.
            default_payload: Updated default payload.
            enabled: Updated active flag.
        """
        body = _update_body(
            name=name,
            schedule=schedule,
            timezone=timezone,
            source_task_id=source_task_id,
            on_status=on_status,
            forward_result=forward_result,
            default_payload=default_payload,
            enabled=enabled,
        )
        response = self._client._request("PATCH", f"/tasks/{task_id}/triggers/{trigger_id}", json=body)
        return Trigger.model_validate(response.json())

    def delete(self, task_id: str, trigger_id: str) -> None:
        """Delete a trigger.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
        """
        self._client._request("DELETE", f"/tasks/{task_id}/triggers/{trigger_id}")


class AsyncTriggersResource:
    """Asynchronous triggers API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(self, task_id: str) -> list[Trigger]:
        """List triggers for a task.

        Args:
            task_id: Parent task ID.

        Returns:
            A list of triggers. Triggers use a simple list (not paginated).
        """
        response = await self._client._request("GET", f"/tasks/{task_id}/triggers")
        body = response.json()
        return [Trigger.model_validate(item) for item in (body.get("items") or [])]

    async def get(self, task_id: str, trigger_id: str) -> Trigger:
        """Get a trigger by ID.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
        """
        response = await self._client._request("GET", f"/tasks/{task_id}/triggers/{trigger_id}")
        return Trigger.model_validate(response.json())

    async def create(
        self,
        task_id: str,
        *,
        name: str,
        type: str,
        schedule: str | None = None,
        timezone: str | None = None,
        source_task_id: str | None = None,
        on_status: str | None = None,
        forward_result: bool | None = None,
        default_payload: Any | None = None,
        enabled: bool | None = None,
    ) -> Trigger:
        """Create a new trigger for a task.

        Args:
            task_id: Parent task ID.
            name: Human-readable trigger label.
            type: Trigger mechanism: HTTP, CRON, EVENT, or QUEUE.
            schedule: Cron expression (required for CRON type).
            timezone: IANA timezone for CRON schedule.
            source_task_id: Source task ID (required for EVENT type).
            on_status: Terminal status filter for EVENT type.
            forward_result: Forward source result as payload for EVENT type.
            default_payload: Optional default JSON payload.
            enabled: Whether the trigger is active. Default: true.
        """
        body = _create_body(
            name=name,
            type=type,
            schedule=schedule,
            timezone=timezone,
            source_task_id=source_task_id,
            on_status=on_status,
            forward_result=forward_result,
            default_payload=default_payload,
            enabled=enabled,
        )
        response = await self._client._request("POST", f"/tasks/{task_id}/triggers", json=body)
        return Trigger.model_validate(response.json())

    async def update(
        self,
        task_id: str,
        trigger_id: str,
        *,
        name: str | None = None,
        schedule: str | None = None,
        timezone: str | None = None,
        source_task_id: str | None = None,
        on_status: str | None = None,
        forward_result: bool | None = None,
        default_payload: Any | None = None,
        enabled: bool | None = None,
    ) -> Trigger:
        """Partially update a trigger. Only provided fields are changed.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
            name: Updated trigger label.
            schedule: Updated cron expression.
            timezone: Updated IANA timezone.
            source_task_id: Updated source task ID.
            on_status: Updated terminal status filter.
            forward_result: Updated result forwarding flag.
            default_payload: Updated default payload.
            enabled: Updated active flag.
        """
        body = _update_body(
            name=name,
            schedule=schedule,
            timezone=timezone,
            source_task_id=source_task_id,
            on_status=on_status,
            forward_result=forward_result,
            default_payload=default_payload,
            enabled=enabled,
        )
        response = await self._client._request("PATCH", f"/tasks/{task_id}/triggers/{trigger_id}", json=body)
        return Trigger.model_validate(response.json())

    async def delete(self, task_id: str, trigger_id: str) -> None:
        """Delete a trigger.

        Args:
            task_id: Parent task ID.
            trigger_id: Trigger ID.
        """
        await self._client._request("DELETE", f"/tasks/{task_id}/triggers/{trigger_id}")


# --- Private helpers ---


def _create_body(
    *,
    name: str,
    type: str,
    schedule: str | None,
    timezone: str | None,
    source_task_id: str | None,
    on_status: str | None,
    forward_result: bool | None,
    default_payload: Any | None,
    enabled: bool | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name, "type": type}
    if schedule is not None:
        body["schedule"] = schedule
    if timezone is not None:
        body["timezone"] = timezone
    if source_task_id is not None:
        body["source_task_id"] = source_task_id
    if on_status is not None:
        body["on_status"] = on_status
    if forward_result is not None:
        body["forward_result"] = forward_result
    if default_payload is not None:
        body["default_payload"] = default_payload
    if enabled is not None:
        body["enabled"] = enabled
    return body


def _update_body(
    *,
    name: str | None,
    schedule: str | None,
    timezone: str | None,
    source_task_id: str | None,
    on_status: str | None,
    forward_result: bool | None,
    default_payload: Any | None,
    enabled: bool | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if schedule is not None:
        body["schedule"] = schedule
    if timezone is not None:
        body["timezone"] = timezone
    if source_task_id is not None:
        body["source_task_id"] = source_task_id
    if on_status is not None:
        body["on_status"] = on_status
    if forward_result is not None:
        body["forward_result"] = forward_result
    if default_payload is not None:
        body["default_payload"] = default_payload
    if enabled is not None:
        body["enabled"] = enabled
    return body
