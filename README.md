# Polyglot AI-Assisted Development Template

A batteries-included **GitHub template** for building full-stack, polyglot applications
with **Claude Code** as a first-class collaborator.

| Layer        | Tech                                                        |
| ------------ | ---------------------------------------------------------- |
| Backend API  | Python 3.13 · FastAPI · SQLAlchemy 2.0 · Alembic · `uv`    |
| Frontend     | TypeScript · React 19 · Vite · Vitest                      |
| Database     | PostgreSQL 17 (local Docker)                                |
| Orchestration| Docker + Docker Compose                                     |
| AI harness   | `.claude/` — rules, skills, subagents, scoped permissions   |

## Why this template

Everything an agent needs to be productive on day one is checked in:

- **`CLAUDE.md`** — the project brief every session loads.
- **`.claude/rules/`** — path-scoped conventions that load only when the relevant
  files enter context (Python rules for `apps/api`, TS rules for `apps/web`, etc.).
- **`.claude/skills/`** — repeatable workflows (`/db-migrate`, `/db-reset`,
  `/new-migration`) so common chores are one command.
- **`.claude/agents/`** — a read-only `code-reviewer` subagent.
- **`.claude/settings.json`** — least-privilege permissions plus format-on-write hooks.

## Layout

```
.
├── apps/
│   ├── api/          # FastAPI backend + Alembic migrations (owns the DB schema)
│   └── web/          # React + Vite frontend
├── .claude/          # Claude Code configuration (committed, shared with the team)
├── .github/          # CI, Dependabot, issue/PR templates
├── docker-compose.yml
├── Makefile          # single entry point for every task
├── CLAUDE.md
└── .env.example
```

## Quick start

```bash
# 0. Use this template on GitHub, then clone your copy.
cp .env.example .env            # fill in / keep the dev defaults

# 1. Bring the whole stack up (postgres + api + web).
make up                          # docker compose up --build -d

# 2. Apply database migrations.
make migrate

# API   → http://localhost:8000  (docs at /docs)
# Web   → http://localhost:5173
# DB    → postgres://localhost:5432
```

Prefer to run a single service on the host? See `apps/api/README.md` and
`apps/web/README.md`.

## Common commands

Everything routes through the `Makefile` so both humans and Claude use one vocabulary:

```bash
make up          # start the stack
make down        # stop the stack
make logs        # tail all logs
make migrate     # apply DB migrations
make revision m="add users"   # generate a new migration
make test        # run api + web test suites
make lint        # run all linters
make fmt         # auto-format everything
make db-reset    # drop, recreate and re-migrate the dev database
```

## Turning this into your project

1. Click **Use this template** on GitHub.
2. Search-and-replace `ccaidtemplate` with your project name.
3. Update `CLAUDE.md` with your domain context.
4. Delete the example `items` resource once you add real features.

## License

MIT — see [LICENSE](LICENSE).
