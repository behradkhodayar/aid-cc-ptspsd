---
paths:
  - "apps/api/**/*.py"
---

# Python / FastAPI conventions

Loaded when working on backend code under `apps/api`.

## Tooling

- **Package manager:** `uv` (not pip/poetry). Add deps with `uv add <pkg>`; dev deps with `uv add --dev <pkg>`.
- **Lint + format:** `ruff` (`ruff check`, `ruff format`). **Type-check:** `mypy src` in strict mode.
- **Tests:** `pytest`. Run via `make api-test`.
- Target **Python 3.13**.

## Style

- Full type hints on every function signature and dataclass/model field. No bare `Any`.
- Prefer `pydantic` models for I/O boundaries and `pydantic-settings` for config — never read `os.environ` directly outside `config.py`.
- Async all the way: route handlers and DB calls are `async`. Use SQLAlchemy 2.0 async sessions.
- Keep routes thin: HTTP concerns in `routes/`, business logic in `services/`, persistence via `models.py` + the session dependency.
- Raise `HTTPException` for client-facing errors; let unexpected errors propagate to the handler.
- Docstrings on public functions: one-line summary, then details if needed.

## Structure

```
src/app/
  main.py       # app factory, middleware, router registration
  config.py     # pydantic-settings Settings, single source of env config
  db.py         # engine, session factory, get_session dependency
  models.py     # SQLAlchemy ORM models
  schemas.py    # pydantic request/response models
  routes/       # one module per resource
```

## Database

- The schema is owned by Alembic migrations under `migrations/`. **Never** `create_all()` in app code
  outside tests, and never hand-edit tables. Generate migrations with `make revision m="..."`.
