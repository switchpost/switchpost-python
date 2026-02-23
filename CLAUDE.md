# SwitchPost Python SDK

Official Python client for the SwitchPost API.

## Package

- **Name**: `switchpost` (PyPI: `switchpost`)
- **Min Python**: 3.11+ (use `X | Y` unions, not `Optional`)
- **Build**: `pyproject.toml` with hatchling
- **Dependencies**: `httpx` (async + sync), `pydantic` for models
- **Dev deps**: `pytest`, `pytest-asyncio`, `ruff`, `mypy`, `respx` (httpx mocking)

## Project Structure

```text
src/switchpost/
  __init__.py          # Re-export SwitchPost, AsyncSwitchPost, all types and errors
  _client.py           # Sync + async client classes (_BaseClient, SwitchPost, AsyncSwitchPost)
  _config.py           # ClientConfig (base_url required, api_key/access_token, timeout, version)
  _errors.py           # SwitchPostError, APIError, AuthenticationError, NotFoundError, etc.
  _pagination.py       # SyncOffsetPage[T], AsyncOffsetPage[T], SyncCursorPage[T], AsyncCursorPage[T]
  _version.py          # __version__
  py.typed             # PEP 561 marker
  types/               # Pydantic models from OpenAPI schemas
    __init__.py
    shared.py          # AuditInfo, CreatedInfo, RateLimit, RetryPolicy, OffsetPaginationMeta, CursorPaginationMeta
    task.py            # Task, CreateTaskInputBody, UpdateTaskInputBody
    trigger.py         # Trigger, CreateTriggerInputBody, UpdateTriggerInputBody
    run.py             # TaskRun, TaskRunAttempt, TaskResultMeta, SubmitRunInputBody
    webhook.py         # Webhook, CreateWebhookInputBody
    principal.py       # Principal, CreatePrincipalInputBody, CreatePrincipalResponse
    binding.py         # PolicyBinding, CreateBindingInputBody
    settings.py        # TenantSettings, SystemSettings
    tenant.py          # Tenant, CreateTenantInputBody, CreateTenantResponse
  resources/           # Resource-specific API methods
    __init__.py
    tasks.py           # TasksResource, AsyncTasksResource
    triggers.py        # TriggersResource, AsyncTriggersResource
    runs.py            # RunsResource, AsyncRunsResource
    attempts.py        # AttemptsResource, AsyncAttemptsResource
    webhooks.py        # WebhooksResource, AsyncWebhooksResource
    principals.py      # PrincipalsResource, AsyncPrincipalsResource
    bindings.py        # BindingsResource, AsyncBindingsResource
    settings.py        # SettingsResource, AsyncSettingsResource
    admin.py           # AdminResource, AsyncAdminResource
tests/
  conftest.py          # Fixtures (client, async_client, mock_api) + response factories
  test_tasks.py
  test_principals.py
  test_client.py
```

## Commands

```bash
uv run pytest                # Run tests
uv run ruff check --fix .    # Lint
uv run ruff format .         # Format
uv run mypy src tests        # Type check
make pre-commit              # Run all checks
```

## API Conventions (from OpenAPI spec)

- **Base URL**: Self-hosted, no default. Must be provided via `base_url` param or `SWITCHPOST_API_URL` env var.
- **Auth**: `X-API-Key` header (for API keys) OR `Authorization: Bearer {token}` (for JWTs). At least one must be provided.
- **Versioning**: `SwitchPost-Version` header, pinned to current API version per SDK release
- **Offset list responses**: `{"items": [...], "offset": N, "limit": N, "total": N}`
- **Cursor list responses**: `{"items": [...], "has_more": bool, "next_cursor": "...", "prev_cursor": "..."}`
- **Simple list responses** (triggers, webhooks, bindings): `{"items": [...]}`
- **Error envelope**: RFC 7807 problem details — `{"status": N, "title": "...", "detail": "...", "type": "...", "errors": [...]}`
- **ID format**: Prefixed Base58 IDs — `tsk_` for tasks, `run_` for runs, `trg_` for triggers, `prn_` for principals, etc.

## SDK Design Patterns

### Client initialization
```python
from switchpost import SwitchPost

# API key authentication
client = SwitchPost(base_url="https://api.example.com", api_key="sp_...")

# Bearer token authentication
client = SwitchPost(base_url="https://api.example.com", access_token="jwt_...")

# From environment variable
# export SWITCHPOST_API_URL=https://api.example.com
client = SwitchPost(api_key="sp_...")

# Async
from switchpost import AsyncSwitchPost
client = AsyncSwitchPost(base_url="https://api.example.com", api_key="sp_...")

# Context manager (recommended)
with SwitchPost(base_url="https://api.example.com", api_key="sp_...") as client:
    task = client.tasks.get("tsk_...")

async with AsyncSwitchPost(base_url="https://api.example.com", api_key="sp_...") as client:
    task = await client.tasks.get("tsk_...")
```

### Resource access (Stripe/Anthropic style)
```python
# List (offset-paginated)
tasks = client.tasks.list(limit=10, offset=0)

# List (cursor-paginated)
runs = client.tasks.list_runs("tsk_...", status="RUNNING", limit=10)

# Get
task = client.tasks.get("tsk_...")

# Create
task = client.tasks.create(name="my-task", endpoint_url="https://example.com/webhook")

# Update (partial)
task = client.tasks.update("tsk_...", timeout_ms=5000)

# Delete
client.tasks.delete("tsk_...")

# Submit run
run = client.tasks.submit_run("tsk_...", payload={"key": "value"})
```

### Error handling
```python
from switchpost import APIError, AuthenticationError, NotFoundError

try:
    task = client.tasks.get("tsk_nonexistent")
except NotFoundError as e:
    print(e.message)       # Human-readable
    print(e.status_code)   # 404
    print(e.title)         # "Not Found"
except APIError as e:
    print(e.error_type)    # URI reference
    print(e.details)       # List of ErrorDetail
```

### Pagination
```python
# Auto-pagination (offset-based)
for task in client.tasks.list():
    print(task.name)

# Auto-pagination (cursor-based)
for run in client.tasks.list_runs("tsk_..."):
    print(run.status)

# Async auto-pagination
async for task in await async_client.tasks.list():
    print(task.name)

# Manual single-page access
page = client.tasks.list(limit=10, offset=0)
print(page.data)          # list[Task]
print(page.pagination)    # OffsetPaginationMeta
```

### Error hierarchy
```
SwitchPostError (base)
+-- APIError (any HTTP error from the API)
|   +-- BadRequestError (400)
|   +-- AuthenticationError (401)
|   +-- PermissionDeniedError (403)
|   +-- NotFoundError (404)
|   +-- ConflictError (409)
|   +-- UnprocessableEntityError (422)
|   +-- RateLimitError (429)
|   +-- InternalServerError (500)
+-- ConnectionError (network-level, including timeouts)
```

## Architecture Notes

### `list` method and builtin shadowing

Resource classes have a method named `list` which shadows Python's builtin `list`
type. This causes mypy `valid-type` errors when later methods in the same class use
`list[str]` in annotations. **Use `typing.List` and `typing.Dict` in resource class
method signatures** — this is the same workaround used by the Anthropic and Stripe
Python SDKs. The private helper functions (outside the class) can use lowercase
`list`/`dict` since there is no shadowing there. Ruff UP006/UP035 are suppressed
via per-file-ignores in `pyproject.toml` for `src/switchpost/resources/*.py`.

Do NOT use `from __future__ import annotations` in resource files — it makes the
problem worse by deferring all annotation evaluation, causing mypy to resolve `list`
to the class method in all cases.

### `ConnectionError` builtin shadowing

`_errors.py` defines `ConnectionError` which shadows Python's builtin. This requires
`# noqa: A001` on the class definition. In `_client.py`, import it aliased:
`from switchpost._errors import ConnectionError as SwitchPostConnectionError`.

### `from __future__ import annotations` policy

- **DO use** in `_client.py`, `_errors.py`, `_pagination.py`, `_config.py`, and test files —
  needed for `TYPE_CHECKING`-guarded forward references and cleaner annotations
- **Do NOT use** in resource files (`resources/*.py`) — it breaks the `list`
  builtin shadowing workaround (see above)

### `TYPE_CHECKING` guards for client types

Resource files and `_pagination.py` reference `SwitchPost` / `AsyncSwitchPost` in type
annotations but don't need them at runtime. These imports are guarded behind
`if TYPE_CHECKING:` to keep the dependency one-directional (`_client.py` ->
resources, never the reverse). In `_pagination.py` and `_client.py`,
`from __future__ import annotations` defers annotation evaluation so the guarded
names resolve. Resource files omit the future import (see `list` shadowing above)
-- the guarded types still work in `__init__` signatures without it.

### Sync/async duplication

Each resource has a sync class and an async class with identical method signatures.
Private helper functions (`_list_params`, `_create_body`, etc.) are shared at module
level to eliminate logic duplication. Method bodies are 2-3 lines each.

### Client `__init__` forwarding

`SwitchPost.__init__` and `AsyncSwitchPost.__init__` use `**kwargs: Any` to forward all
parameters to `_BaseClient.__init__`, avoiding duplicating the parameter list
(base_url, api_key, access_token, timeout, version, max_retries) in three places.

### Dual authentication

SwitchPost supports two auth methods:
- `api_key` -> sent as `X-API-Key` header
- `access_token` -> sent as `Authorization: Bearer {token}` header

At least one must be provided. Both can be provided simultaneously.

### No default base URL

SwitchPost is self-hosted. There is no default base URL. The `base_url` parameter
is required unless the `SWITCHPOST_API_URL` environment variable is set.

### Pagination internals

SwitchPost uses two pagination styles:
- **Offset pagination** (tasks, principals): `SyncOffsetPage[T]` / `AsyncOffsetPage[T]`
- **Cursor pagination** (runs, attempts): `SyncCursorPage[T]` / `AsyncCursorPage[T]`
- **Simple lists** (triggers, webhooks, bindings): Return `list[T]` directly (no pagination wrapper)

`_pagination.py` uses `from __future__ import annotations` for forward-reference
resolution of `TYPE_CHECKING`-guarded client types.

### Test imports

Test files import conftest helpers as `from conftest import ...` (not
`from tests.conftest import ...`) because `tests/` is not a package on `sys.path`.
pytest makes conftest importable within the test directory automatically.

### Test factories

`conftest.py` provides factory functions for building mock responses:

- `task_json(**overrides)` / `principal_json(**overrides)` / `run_json(**overrides)` — single entity dicts
- `offset_list_response(items, offset, limit, total)` — offset-paginated list envelope
- `cursor_list_response(items, has_more, next_cursor, prev_cursor)` — cursor-paginated list envelope
- `error_response(status, title, detail, type, errors)` — RFC 7807 error envelope

All accept `**overrides` for field customization. Use `respx.mock(base_url=...)`.

## Adding a New Resource

1. Add Pydantic models in `types/<resource>.py`, re-export from `types/__init__.py`
2. Create `resources/<resource>.py` with sync + async classes and private helpers.
   Use `typing.List`/`typing.Dict` in class method signatures (not lowercase)
3. Register on both client classes in `_client.py` (type annotation + `__init__`)
4. Re-export new types from `__init__.py` and add to `__all__`
5. Add `<resource>_json()` factory to `tests/conftest.py`
6. Write tests in `tests/test_<resource>.py`

## Style

- Python 3.11+ — use `X | Y` unions, not `Optional`
- All public methods return typed Pydantic models
- Both sync (`SwitchPost`) and async (`AsyncSwitchPost`) clients with context manager support
- httpx for HTTP — supports connection pooling, retries, timeouts
- respx for test mocking (not requests-mock)
- Follow Anthropic SDK patterns for naming and structure
- Docstrings on all public methods with parameter descriptions
- `__all__` exports in every `__init__.py`
- Line length: 120
- ruff for linting/formatting, mypy strict mode for type checking

## API Version Pinning

The SDK pins `DEFAULT_VERSION` in `_config.py` to a specific API version (currently
`"0.0.0"` matching the spec). This is sent as the `SwitchPost-Version` header on every
request, ensuring deterministic API behavior for SDK users regardless of server-side changes.

**Never use `"latest"` as the default.** Each SDK release must target a known API
version. When the API introduces a new version, update `DEFAULT_VERSION` to the new
value and adjust types/resources to match.

## Reference

- OpenAPI spec: `openapi.json` in repo root
- The spec is the source of truth for all types, endpoints, and error shapes
