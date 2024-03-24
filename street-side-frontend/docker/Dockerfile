ARG PROJECT_NAME_FOLDER=street-side
ARG TOP_FOLDER=/opt/${PROJECT_NAME_FOLDER}
ARG APP_FOLDER=street-side-frontend
ARG APP_NAME=street_side_api
ARG NODE_VERSION=21

FROM node:${NODE_VERSION}-bookworm-slim AS base

FROM base as dependencies
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

RUN apk add --no-cache libc6-compat
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY package.json package-lock.json* ./

RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
    else echo "Lockfile not found." && exit 1; \
    fi


# Rebuild the source code only when needed
FROM base AS builder
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY --from=deps /${TOP_FOLDER}/${APP_FOLDER}/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN \
    if [ -f yarn.lock ]; then yarn run build; \
    elif [ -f package-lock.json ]; then npm run build; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
    else echo "Lockfile not found." && exit 1; \
    fi

# Production image, copy all the files and run next
FROM base AS runner
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

ENV NODE_ENV production
# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /${TOP_FOLDER}/${APP_FOLDER}/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /${TOP_FOLDER}/${APP_FOLDER}/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /${TOP_FOLDER}/${APP_FOLDER}/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/next-config-js/output
CMD HOSTNAME="0.0.0.0" node server.js