---
paths:
  - "apps/api/migrations/**"
  - "apps/api/**/models.py"
  - "**/*.sql"
---

# Database & migration conventions

Loaded when touching migrations, ORM models, or SQL. PostgreSQL 17, schema owned by the API.

## Rules

- **Alembic is the only way the schema changes.** No manual `ALTER TABLE`, no `create_all()` in prod code.
- Generate migrations from model changes: edit `models.py`, then `make revision m="describe change"`,
  then **review the generated file** — autogenerate misses server defaults, enum changes, and data moves.
- Every migration must implement **both `upgrade()` and `downgrade()`**. If a change is truly
  irreversible, say so explicitly in `downgrade()` with a raised error and a comment.
- Never edit a migration that has already been applied on a shared branch — add a new one.
- Prefer additive, backwards-compatible steps (add nullable column → backfill → enforce not-null)
  so deploys don't require downtime.

## Conventions

- Table names: plural snake_case (`items`, `user_accounts`). Primary key `id`.
- Include `created_at` / `updated_at` (`timestamptz`, server default `now()`) on every table.
- Money as `numeric`, never float. Timestamps always timezone-aware.
- Add indexes for every foreign key and every column used in a `WHERE`/`ORDER BY` hot path.

## Applying

- `make migrate` upgrades to head. `make db-reset` drops the volume and rebuilds from scratch (dev only).
