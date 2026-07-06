# API — FastAPI backend

Python 3.14 · FastAPI · SQLAlchemy 2.0 (async) · Alembic · `uv`.

Owns the database schema. The web app talks to it over HTTP; nothing else touches Postgres directly.

## Run inside the stack (recommended)

From the repo root:

```bash
make up        # starts db + api + web
make migrate   # apply migrations
```

API docs: <http://localhost:8000/docs>.

## Run on the host

```bash
cd apps/api
uv sync --all-extras --dev
cp .env.example .env          # point DATABASE_URL at localhost
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --app-dir src
```

## Layout

```
src/app/
  main.py       app factory + middleware + router registration
  config.py     pydantic-settings — the only reader of env config
  db.py         async engine, session factory, get_session dependency
  models.py     SQLAlchemy ORM models (schema mirrored by Alembic)
  schemas.py    pydantic request/response models (the HTTP contract)
  routes/       one module per resource (health, items)
migrations/     Alembic — the only way the schema changes
tests/          pytest (async), one file per route module
```

## Common tasks

| Task              | Command                             |
| ----------------- | ----------------------------------- |
| New migration     | `make revision m="add users table"` |
| Apply migrations  | `make migrate`                      |
| Test              | `make api-test` / `uv run pytest`   |
| Lint + type-check | `make api-lint`                     |
| Format            | `make api-fmt`                      |

## Adding a resource

1. Add the ORM model to `models.py`.
2. `make revision m="add <thing>"`, then review the generated migration.
3. Add pydantic schemas to `schemas.py`.
4. Add a `routes/<thing>.py` router and register it in `main.py`.
5. Add tests in `tests/test_<thing>.py`.
6. Update `apps/web/src/api.ts` if the web app consumes it.
