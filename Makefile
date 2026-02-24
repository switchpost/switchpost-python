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
