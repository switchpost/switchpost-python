# SwitchPost Python Library

[![CI](https://github.com/switchpost/switchpost-python/actions/workflows/ci.yml/badge.svg)](https://github.com/switchpost/switchpost-python/actions/workflows/ci.yml)

The SwitchPost Python library provides convenient access to the SwitchPost API from Python 3.11+. It includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Installation

```sh
pip install switchpost
```

## Usage

```python
from switchpost import SwitchPost

client = SwitchPost(base_url="https://switchpost.example.com", api_key="sp_...")

# List tasks
for task in client.tasks.list():
    print(task.name)

# Get a single task
task = client.tasks.get("tsk_4K7fR9pLm2nQwXvY8cJH3")

# Create a task
task = client.tasks.create(
    name="my-webhook-task",
    endpoint_url="https://example.com/webhook",
)

# Update a task
task = client.tasks.update("tsk_4K7fR9pLm2nQwXvY8cJH3", timeout_ms=5000)

# Delete a task
client.tasks.delete("tsk_4K7fR9pLm2nQwXvY8cJH3")
```

We recommend using a context manager to ensure connections are cleaned up:

```python
with SwitchPost(base_url="https://switchpost.example.com", api_key="sp_...") as client:
    task = client.tasks.get("tsk_4K7fR9pLm2nQwXvY8cJH3")
```

## Authentication

SwitchPost supports two authentication methods:

```python
# API key (X-API-Key header)
client = SwitchPost(base_url="https://...", api_key="sp_...")

# Bearer token (Authorization header)
client = SwitchPost(base_url="https://...", access_token="jwt_token_here")

# Both can be provided simultaneously
client = SwitchPost(base_url="https://...", api_key="sp_...", access_token="jwt_...")
```

At least one of `api_key` or `access_token` must be provided.

## Base URL

SwitchPost is self-hosted -- there is no default API URL. You must provide one:

```python
# Via constructor parameter
client = SwitchPost(base_url="https://switchpost.example.com", api_key="sp_...")

# Or via environment variable
# export SWITCHPOST_API_URL=https://switchpost.example.com
client = SwitchPost(api_key="sp_...")
```

## Async usage

Import `AsyncSwitchPost` instead of `SwitchPost` and use `await` with each API call:

```python
import asyncio
from switchpost import AsyncSwitchPost


async def main():
    async with AsyncSwitchPost(base_url="https://switchpost.example.com", api_key="sp_...") as client:
        task = await client.tasks.get("tsk_4K7fR9pLm2nQwXvY8cJH3")
        print(task.name)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is identical.

## Task runs

Submit and manage task runs:

```python
# Submit a run
run = client.tasks.submit_run("tsk_...", payload={"key": "value"})

# List runs for a task (cursor-paginated)
for run in client.tasks.list_runs("tsk_...", status="RUNNING"):
    print(f"{run.id}: {run.status}")

# Get run details
run = client.runs.get("run_...")

# Cancel a running task
run = client.runs.cancel("run_...")

# Retry a failed run
run = client.runs.retry("run_...")

# Get result metadata
result = client.runs.get_result("run_...")
print(result.blob_url)
```

## Triggers

Manage task triggers (HTTP, CRON, EVENT, QUEUE):

```python
# Create a cron trigger
trigger = client.triggers.create(
    "tsk_...",
    name="Daily sync",
    type="CRON",
    schedule="0 9 * * *",
    timezone="America/New_York",
)

# List triggers
triggers = client.triggers.list("tsk_...")

# Update a trigger
trigger = client.triggers.update("tsk_...", "trg_...", enabled=False)

# Delete a trigger
client.triggers.delete("tsk_...", "trg_...")
```

## Principals and RBAC

Manage principals (API keys, users) and their policy bindings:

```python
# Create an API key principal
result = client.principals.create(type="api_key", name="CI Pipeline")
print(result.api_key)       # Save this -- shown only once
print(result.principal.id)  # prn_...

# List principals
for principal in client.principals.list():
    print(f"{principal.name} ({principal.type})")

# Create a policy binding
binding = client.bindings.create(
    "prn_...",
    role="admin",
    resource_type="tenant",
    resource_id="tnt_...",
)

# List bindings for a principal
bindings = client.bindings.list("prn_...")
```

## Pagination

List methods return a page that supports automatic pagination:

```python
# Auto-paginate through all results (offset-based)
for task in client.tasks.list():
    print(task.name)

# Auto-paginate (cursor-based)
for run in client.tasks.list_runs("tsk_..."):
    print(run.status)

# Async auto-pagination
async for task in await async_client.tasks.list():
    print(task.name)
```

You can also access a single page directly:

```python
# Offset-paginated
page = client.tasks.list(limit=10, offset=0)
print(page.data)        # list[Task]
print(page.pagination)  # OffsetPaginationMeta (offset, limit, total)

# Cursor-paginated
page = client.tasks.list_runs("tsk_...", limit=10)
print(page.data)        # list[TaskRun]
print(page.pagination)  # CursorPaginationMeta (has_more, next_cursor, prev_cursor)
```

## Handling errors

When the API returns a non-success status code, a subclass of `APIError` is raised:

```python
from switchpost import SwitchPost, NotFoundError, AuthenticationError, APIError

client = SwitchPost(base_url="https://...", api_key="sp_...")

try:
    client.tasks.get("tsk_nonexistent00000000")
except NotFoundError as e:
    print(e.message)       # Human-readable error message
    print(e.status_code)   # 404
    print(e.title)         # "Not Found"
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(e.status_code)
    print(e.error_type)
    print(e.details)       # List of ErrorDetail, if any
```

When the library cannot reach the API (network issues, timeouts), a `ConnectionError` is raised.

### Error types

| Status Code | Error Type               |
| ----------- | ------------------------ |
| 400         | `BadRequestError`        |
| 401         | `AuthenticationError`    |
| 403         | `PermissionDeniedError`  |
| 404         | `NotFoundError`          |
| 409         | `ConflictError`          |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`         |
| 500         | `InternalServerError`    |
| N/A         | `ConnectionError`        |

All errors inherit from `SwitchPostError`.

## Configuration

### Timeouts

The default timeout is 60 seconds. You can override it:

```python
client = SwitchPost(base_url="https://...", api_key="sp_...", timeout=30.0)
```

On timeout, a `ConnectionError` is raised.

### API versioning

Each SDK release is pinned to a specific API version. You can override it, but be aware that the types may not match:

```python
client = SwitchPost(base_url="https://...", api_key="sp_...", version="0.0.0")
```

## Types

All responses are [Pydantic](https://docs.pydantic.dev) models with full type annotations. This gives you autocomplete, type checking, and serialization out of the box:

```python
task = client.tasks.get("tsk_...")

task.id              # str
task.name            # str
task.endpoint_url    # str
task.retry_policy    # RetryPolicy
task.audit           # AuditInfo
```

### Determining the installed version

```python
import switchpost
print(switchpost.__version__)
```

## Versioning

This package follows [SemVer](https://semver.org/spec/v2.0.0.html). Backwards-incompatible changes are released as major versions.

## Requirements

Python 3.11+.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
