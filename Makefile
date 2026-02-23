.PHONY: fetch-openapi test ruff-check ruff-format mypy pre-commit install-pre-commit fetch-features e2e e2e-run

fetch-openapi:
	bash scripts/fetch-openapi.sh

test:
	uv run pytest

ruff-check:
	uv run ruff check --fix .

ruff-format:
	uv run ruff format .

mypy:
	uv run mypy src tests

pre-commit: ruff-format ruff-check mypy test

install-pre-commit:
	uv tool install pre-commit --with pre-commit-uv && uv run pre-commit install

fetch-features:
	bash scripts/fetch-features.sh

e2e: fetch-features
	docker compose -f docker-compose.e2e.yml up -d --wait
	bash scripts/e2e-bootstrap.sh
	set -a && . .env.e2e && set +a && $(MAKE) e2e-run
	docker compose -f docker-compose.e2e.yml down -v

e2e-run:
	uv run pytest tests/e2e/ -v
