# Single entry point for humans and Claude. `make help` lists everything.
.DEFAULT_GOAL := help
COMPOSE := docker compose

.PHONY: help up down restart logs ps build \
        migrate revision db-reset db-shell \
        test api-test web-test lint api-lint web-lint fmt api-fmt web-fmt \
        api-shell web-shell install skills-scan

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

## ---- Stack ----
up: ## Build and start the full stack (db + api + web)
	$(COMPOSE) up --build -d
	@echo "API  → http://localhost:8000/docs"
	@echo "Web  → http://localhost:5173"

down: ## Stop the stack
	$(COMPOSE) down

restart: down up ## Restart the stack

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

ps: ## Show running services
	$(COMPOSE) ps

build: ## Rebuild images without starting
	$(COMPOSE) build

## ---- Database (Alembic lives in apps/api) ----
migrate: ## Apply all pending migrations
	$(COMPOSE) run --rm api alembic upgrade head

revision: ## Create a migration: make revision m="add users table"
	$(COMPOSE) run --rm api alembic revision --autogenerate -m "$(m)"

db-reset: ## Drop, recreate and re-migrate the dev database
	$(COMPOSE) down -v
	$(COMPOSE) up -d db
	$(COMPOSE) run --rm api alembic upgrade head

db-shell: ## Open a psql shell
	$(COMPOSE) exec db psql -U $${POSTGRES_USER:-app} -d $${POSTGRES_DB:-app}

## ---- Tests ----
test: api-test web-test ## Run all test suites

api-test: ## Run backend tests
	$(COMPOSE) run --rm api pytest

web-test: ## Run frontend tests
	$(COMPOSE) run --rm web pnpm test

## ---- Lint & format ----
lint: api-lint web-lint ## Lint everything

api-lint: ## Lint + type-check the backend
	$(COMPOSE) run --rm api sh -c "ruff check . && mypy src"

web-lint: ## Lint + type-check the frontend
	$(COMPOSE) run --rm web sh -c "pnpm lint && pnpm typecheck"

fmt: api-fmt web-fmt ## Auto-format everything

api-fmt: ## Format backend code
	$(COMPOSE) run --rm api ruff format .

web-fmt: ## Format frontend code
	$(COMPOSE) run --rm web pnpm format

## ---- Shells ----
api-shell: ## Shell into the api container
	$(COMPOSE) exec api sh

web-shell: ## Shell into the web container
	$(COMPOSE) exec web sh

## ---- Agent harness ----
skills-scan: ## Scan .claude/skills with NVIDIA SkillSpector (opt-in; needs uv on the host)
	@command -v uv >/dev/null 2>&1 || { echo "uv is required: https://docs.astral.sh/uv/"; exit 1; }
	@for d in .claude/skills/*/; do \
		echo "== $$d"; \
		uvx --from git+https://github.com/NVIDIA/skillspector.git skillspector scan "$$d" || exit 1; \
	done
