# Web — React + Vite frontend

TypeScript · React 19 · Vite · Vitest. A pure client of the API — no direct DB access.

## Run inside the stack (recommended)

From the repo root, `make up` starts this at <http://localhost:5173> with HMR.

## Run on the host

```bash
cd apps/web
pnpm install
cp .env.example .env      # point VITE_API_URL at the running API
pnpm dev
```

## Layout

```
src/
  main.tsx        entrypoint, mounts <App/>
  App.tsx         root component
  api.ts          the ONLY place that talks to the backend (typed client)
  *.test.tsx      colocated Vitest + Testing Library tests
```

## Conventions

- **Strict TypeScript, no `any`.** Named exports only.
- All network calls live in `src/api.ts`; components import typed functions from it.
- Keep the interfaces in `api.ts` in sync with `apps/api/src/app/schemas.py` — that's the contract.
- Config comes from `import.meta.env.VITE_*`; never hardcode the API URL.

## Commands

| Task              | Command                          |
| ----------------- | -------------------------------- |
| Dev server        | `pnpm dev` / `make up`           |
| Test              | `pnpm test` / `make web-test`    |
| Lint + type-check | `make web-lint`                  |
| Format            | `pnpm format` / `make web-fmt`   |
| Production build  | `pnpm build`                     |
