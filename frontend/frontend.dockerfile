FROM docker.io/node:22.12-alpine3.21 AS base

# Install dependencies only when needed
FROM base AS deps

RUN apk update
RUN apk upgrade
RUN apk add --no-cache libc6-compat bash
WORKDIR /app

COPY package.json package-lock.json* ./
RUN \
  if [ -f package-lock.json ]; then npm ci; \
  else npm install && exit 1; \
  fi

FROM base AS dev

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE ${PORT_FRONTEND}