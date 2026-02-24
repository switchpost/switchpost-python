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

from typing import Any

import httpx
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """A single validation or field-level error detail from the API."""

    location: str | None = None
    message: str | None = None
    value: Any | None = None


class SwitchPostError(Exception):
    """Base exception for all SwitchPost SDK errors."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(SwitchPostError):
    """An error response from the SwitchPost API."""

    status_code: int
    error_type: str | None
    title: str | None
    instance: str | None
    details: list[ErrorDetail] | None

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_type: str | None = None,
        title: str | None = None,
        instance: str | None = None,
        details: list[ErrorDetail] | None = None,
    ) -> None:
        self.status_code = status_code
        self.error_type = error_type
        self.title = title
        self.instance = instance
        self.details = details
        super().__init__(message)


class BadRequestError(APIError):
    """400 Bad Request."""


class AuthenticationError(APIError):
    """401 Unauthorized."""


class PermissionDeniedError(APIError):
    """403 Forbidden."""


class NotFoundError(APIError):
    """404 Not Found."""


class ConflictError(APIError):
    """409 Conflict."""


class UnprocessableEntityError(APIError):
    """422 Unprocessable Entity."""


class RateLimitError(APIError):
    """429 Too Many Requests."""


class InternalServerError(APIError):
    """500 Internal Server Error."""


class ConnectionError(SwitchPostError):  # noqa: A001
    """Network-level error (timeout, DNS, connection refused)."""


_STATUS_CODE_MAP: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
    500: InternalServerError,
}


def _make_api_error(response: httpx.Response) -> APIError:
    """Parse an error response and return the appropriate APIError subclass.

    SwitchPost uses RFC 7807 problem details format:
    ``{"status": N, "title": "...", "detail": "...", "type": "...", "errors": [...]}``
    """
    status_code = response.status_code
    error_cls = _STATUS_CODE_MAP.get(status_code, APIError)

    try:
        body: dict[str, Any] = response.json()
    except Exception:
        return error_cls(
            message=response.text or f"HTTP {status_code}",
            status_code=status_code,
        )

    message = body.get("detail", body.get("title", response.text or f"HTTP {status_code}"))
    error_type = body.get("type")
    title = body.get("title")
    instance = body.get("instance")

    details: list[ErrorDetail] | None = None
    raw_errors = body.get("errors")
    if raw_errors is not None:
        details = [ErrorDetail.model_validate(e) for e in raw_errors]

    return error_cls(
        message=message,
        status_code=status_code,
        error_type=error_type,
        title=title,
        instance=instance,
        details=details,
    )
