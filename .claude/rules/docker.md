---
paths:
  - "**/Dockerfile"
  - "**/docker-compose*.yml"
  - "**/.dockerignore"
---

# Docker conventions

Loaded when editing Dockerfiles or compose config.

## Rules

- **Multi-stage builds.** A `dev` target with hot-reload tooling and source mounts; a lean `runtime`
  target for anything shipped. Never bake dev dependencies into the runtime stage.
- **Pin base images** to a major version and prefer `-slim` / `-alpine` (`python:3.13-slim`,
  `node:24-alpine`, `postgres:17-alpine`).
- **Run as a non-root user** in the runtime stage.
- Order layers cheap-to-expensive: copy dependency manifests and install *before* copying source,
  so code edits don't bust the dependency cache.
- Keep `.dockerignore` tight — never send `.git`, `node_modules`, `.venv`, or `.env` into the build context.
- Add a `HEALTHCHECK` (or a compose `healthcheck`) to every long-running service.

## Compose

- Services talk to each other by **service name** (`db`, `api`), not `localhost`.
- Secrets/config come from `.env` via `env_file` or `environment:` — never hardcoded in the compose file.
- Gate startup order with `depends_on` + `condition: service_healthy`, not `sleep`.
