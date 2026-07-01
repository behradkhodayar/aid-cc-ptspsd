---
description: Destroy and rebuild the local dev database from scratch, then re-apply all migrations
disable-model-invocation: true
argument-hint: (no args)
---

⚠️ **Destructive — dev only.** This drops the Postgres volume and all local data.

Confirm the user really wants to wipe local data, then run:

```bash
make db-reset
```

This will:
1. `docker compose down -v` (removes the `pgdata` volume — all rows gone).
2. Recreate the `db` service.
3. `alembic upgrade head` to rebuild the schema from migrations.

After it completes, report that the database is back at head with an empty schema. Never run this
against anything but a local development database.
