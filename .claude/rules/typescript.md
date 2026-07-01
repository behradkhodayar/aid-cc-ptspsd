---
paths:
  - "apps/web/**/*.ts"
  - "apps/web/**/*.tsx"
---

# TypeScript / React conventions

Loaded when working on frontend code under `apps/web`.

## Tooling

- **Package manager:** `pnpm`. **Bundler/dev server:** Vite. **Tests:** Vitest + Testing Library.
- **Lint:** ESLint (flat config). **Format:** Prettier. **Type-check:** `tsc --noEmit` (`pnpm typecheck`).
- Run via `make web-test`, `make web-lint`, `make web-fmt`.

## Style

- **Strict TypeScript.** No `any` — reach for `unknown` + narrowing, generics, or a precise type.
- **Named exports only**, never `export default` (except where a framework demands it).
- Function components with hooks; no class components.
- Co-locate tests: `Foo.tsx` → `Foo.test.tsx`.
- Keep all network access in `src/api.ts`; components call typed functions, never `fetch` inline.
- Read config from `import.meta.env.VITE_*` — never hardcode URLs or ports.
- Prefer small, composable components; lift shared types into a `types.ts` when they're reused.

## The API contract

`src/api.ts` is the single boundary to the backend. When the FastAPI response shape changes,
update the TypeScript types here in the same change so the contract stays honest.
