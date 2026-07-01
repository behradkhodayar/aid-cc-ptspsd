---
description: Apply pending Alembic database migrations to the running Postgres container
disable-model-invocation: false
---

## Current migration state

!`docker compose run --rm api alembic current 2>/dev/null || echo "(stack not running — start it with 'make up')"`

## Task

Apply all pending database migrations by running:

```bash
make migrate
```

Then confirm success by checking `alembic current` matches `alembic heads`. If the migration
fails, read the error, inspect the offending migration in `apps/api/migrations/versions/`, and
report the root cause before attempting a fix. Do not edit an already-applied migration — add a
new one instead.
