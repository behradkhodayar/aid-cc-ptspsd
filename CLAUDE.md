# Project conventions

Polyglot full-stack app: **Python/FastAPI** backend, **TypeScript/React** frontend,
**PostgreSQL** in Docker. This file loads every session — keep it short. Language- and
path-specific detail lives in `.claude/rules/` and loads on demand.

## Commands (always prefer the Makefile)

- Start stack: `make up` · Stop: `make down` · Logs: `make logs`
- Test everything: `make test` · Lint: `make lint` · Format: `make fmt`
- DB migrate: `make migrate` · New migration: `make revision m="msg"` · Reset: `make db-reset`
- Backend only: `make api-test`, `make api-lint`
- Frontend only: `make web-test`, `make web-lint`

## Architecture

- `apps/api` — FastAPI service. **Owns the database schema** via Alembic migrations.
- `apps/web` — React + Vite SPA. Talks to the API over HTTP; never touches the DB directly.
- `db` — PostgreSQL 17, run through Docker Compose. Schema changes go through Alembic, never manual SQL.
- The API is the single source of truth for data; the web app is a pure client.

## Ground rules

- **Never edit the database schema by hand.** Add an Alembic migration (`make revision`).
- **Never commit secrets.** Config comes from env vars; `.env` is gitignored, `.env.example` is the contract.
- Keep the API and web app decoupled — the only coupling is the HTTP contract in `apps/web/src/api.ts`.
- Tests live next to the code they cover (`test_*.py` for Python, `*.test.tsx` for TS).
- Follow the branch → PR → review → squash-merge flow; never push directly to `main`.
- Third-party skills are untrusted code: vet with `make skills-scan` and see
  `docs/ecosystem.md` before adopting any.

## When you touch...

- Python (`apps/api/**`) → the Python rule loads automatically. Use `uv`, `ruff`, type hints.
- TypeScript (`apps/web/**`) → the TS rule loads. Named exports, strict mode, no `any`.
- Migrations / SQL → the database rule loads. Reversible migrations only.
- Docker / compose → the docker rule loads.
