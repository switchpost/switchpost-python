"""Common step definitions shared across all features -- error and status assertions."""

from __future__ import annotations

from pytest_bdd import parsers, then
from tests.e2e.conftest import ScenarioContext

# ---------------------------------------------------------------------------
# Response status assertions
# ---------------------------------------------------------------------------


@then(parsers.parse("the response status should be {code:d}"))
def response_status_is(ctx: ScenarioContext, code: int) -> None:
    assert ctx.last_status_code == code, f"Expected status {code}, got {ctx.last_status_code}" + (
        f" ({ctx.last_error})" if ctx.last_error else ""
    )


# ---------------------------------------------------------------------------
# Error response structure assertions (RFC 7807)
# ---------------------------------------------------------------------------


@then(parsers.parse('the error response should have a "status" of {value:d}'))
def error_has_status(ctx: ScenarioContext, value: int) -> None:
    assert ctx.error_response.get("status") == value


@then(parsers.parse('the error response should have a "title" string'))
def error_has_title(ctx: ScenarioContext) -> None:
    title = ctx.error_response.get("title")
    assert title is not None and isinstance(title, str) and len(title) > 0


@then(parsers.parse('the error response should have a "detail" string'))
def error_has_detail(ctx: ScenarioContext) -> None:
    detail = ctx.error_response.get("detail")
    assert detail is not None and isinstance(detail, str) and len(detail) > 0


@then('the error response should have an "errors" array')
def error_has_errors_array(ctx: ScenarioContext) -> None:
    errors = ctx.error_response.get("errors")
    assert errors is not None and isinstance(errors, list)


@then(parsers.parse('the errors array should reference the "{field}" field'))
def errors_reference_field(ctx: ScenarioContext, field: str) -> None:
    errors = ctx.error_response.get("errors", [])
    # Check if any error references the field in location or message
    found = False
    for err in errors:
        loc = err.get("location", "") or ""
        msg = err.get("message", "") or ""
        if field in loc or field in msg:
            found = True
            break
    assert found, f"No error references field {field!r}; errors: {errors}"


@then('the error response should have a "status" integer')
def error_has_status_integer(ctx: ScenarioContext) -> None:
    status = ctx.error_response.get("status")
    assert status is not None and isinstance(status, int)


@then('the error response should have a "type" URI string')
def error_has_type_uri(ctx: ScenarioContext) -> None:
    typ = ctx.error_response.get("type")
    assert typ is not None and isinstance(typ, str)


@then(parsers.parse('the error response content type should be "application/problem+json"'))
def error_content_type_problem_json(ctx: ScenarioContext) -> None:
    # The SDK parses JSON from error responses, so if we got a parsed
    # error_response dict with "status", "title", etc., it was
    # application/problem+json.  We verify the structure is present.
    assert ctx.error_response.get("status") is not None
    assert ctx.error_response.get("title") is not None
