---
description: Generate a new Alembic migration from current model changes and review it
argument-hint: <short description of the change>
disable-model-invocation: false
---

Generate a new database migration for: **$ARGUMENTS**

Steps:

1. Make sure the intended change is reflected in `apps/api/src/app/models.py` first — Alembic
   autogenerate diffs the ORM models against the live database.
2. Generate the migration:
   ```bash
   make revision m="$ARGUMENTS"
   ```
3. **Open the newly created file** under `apps/api/migrations/versions/` and review it carefully:
   - Does `upgrade()` capture the full intent? Autogenerate misses server defaults, enum value
     changes, index renames, and data backfills.
   - Is `downgrade()` correct and reversible?
   - For column additions on a non-empty table, is the column nullable or given a server default?
4. Apply it with `make migrate` and confirm it succeeds.
5. Summarize what the migration does and any manual edits you made to the generated file.
