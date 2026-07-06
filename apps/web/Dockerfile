# syntax=docker/dockerfile:1

# ---- base: node + pnpm ----
FROM node:24-alpine AS base
WORKDIR /app
# pnpm version comes from package.json's packageManager field — the single source of
# truth. Not corepack: Node stopped shipping it in images >= 25 (see issue #12).
COPY package.json ./
RUN npm install -g "$(node -p 'require("./package.json").packageManager')"

# ---- deps: install from lockfile, cached ----
FROM base AS deps
COPY package.json pnpm-lock.yaml* ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile || pnpm install

# ---- dev: Vite dev server with HMR (source bind-mounted by compose) ----
FROM deps AS dev
COPY . .
EXPOSE 5173
CMD ["pnpm", "dev"]

# ---- build: produce static assets ----
FROM deps AS build
COPY . .
RUN pnpm build

# ---- runtime: static files served by nginx, non-root ----
FROM nginx:1.31-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --retries=5 \
    CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
