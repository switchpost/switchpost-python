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

from typing import TYPE_CHECKING, Any

from switchpost.types.binding import PolicyBinding

if TYPE_CHECKING:
    from switchpost._client import AsyncSwitchPost, SwitchPost


class BindingsResource:
    """Synchronous policy bindings API."""

    def __init__(self, client: "SwitchPost") -> None:
        self._client = client

    def list(self, principal_id: str) -> list[PolicyBinding]:
        """List policy bindings for a principal.

        Args:
            principal_id: Principal ID.

        Returns:
            A list of policy bindings.
        """
        response = self._client._request("GET", f"/principals/{principal_id}/bindings")
        body = response.json()
        return [PolicyBinding.model_validate(item) for item in (body.get("items") or [])]

    def create(
        self,
        principal_id: str,
        *,
        role: str,
        resource_type: str,
        resource_id: str,
    ) -> PolicyBinding:
        """Create a policy binding for a principal.

        Args:
            principal_id: Principal ID.
            role: Role to grant.
            resource_type: Resource type: ``tenant`` or ``task``.
            resource_id: Resource ID to scope the binding to.
        """
        body = _create_body(role=role, resource_type=resource_type, resource_id=resource_id)
        response = self._client._request("POST", f"/principals/{principal_id}/bindings", json=body)
        return PolicyBinding.model_validate(response.json())

    def delete(self, binding_id: str) -> None:
        """Delete a policy binding.

        Args:
            binding_id: Binding ID.
        """
        self._client._request("DELETE", f"/bindings/{binding_id}")


class AsyncBindingsResource:
    """Asynchronous policy bindings API."""

    def __init__(self, client: "AsyncSwitchPost") -> None:
        self._client = client

    async def list(self, principal_id: str) -> list[PolicyBinding]:
        """List policy bindings for a principal.

        Args:
            principal_id: Principal ID.

        Returns:
            A list of policy bindings.
        """
        response = await self._client._request("GET", f"/principals/{principal_id}/bindings")
        body = response.json()
        return [PolicyBinding.model_validate(item) for item in (body.get("items") or [])]

    async def create(
        self,
        principal_id: str,
        *,
        role: str,
        resource_type: str,
        resource_id: str,
    ) -> PolicyBinding:
        """Create a policy binding for a principal.

        Args:
            principal_id: Principal ID.
            role: Role to grant.
            resource_type: Resource type: ``tenant`` or ``task``.
            resource_id: Resource ID to scope the binding to.
        """
        body = _create_body(role=role, resource_type=resource_type, resource_id=resource_id)
        response = await self._client._request("POST", f"/principals/{principal_id}/bindings", json=body)
        return PolicyBinding.model_validate(response.json())

    async def delete(self, binding_id: str) -> None:
        """Delete a policy binding.

        Args:
            binding_id: Binding ID.
        """
        await self._client._request("DELETE", f"/bindings/{binding_id}")


# --- Private helpers ---


def _create_body(*, role: str, resource_type: str, resource_id: str) -> dict[str, Any]:
    return {"role": role, "resource_type": resource_type, "resource_id": resource_id}
