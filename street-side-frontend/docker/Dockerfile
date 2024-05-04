ARG PROJECT_NAME_FOLDER=street-side
ARG TOP_FOLDER=/opt/${PROJECT_NAME_FOLDER}
ARG APP_FOLDER=street-side-frontend
ARG APP_NAME=street_side_api
ARG NODE_VERSION=21

FROM node:${NODE_VERSION}-bookworm-slim AS base

# Rebuild the source code only when needed
FROM base AS builder
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/.eslintrc.json ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/next.config.mjs ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/package-lock.json ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/package.json ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/postcss.config.js ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/README.md ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/tailwind.config.ts ./
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/tsconfig.json ./

RUN npm install;

# Dev image, copy all the files and run next
FROM builder AS development
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/docker/dev-entrypoint.sh docker/entrypoint.sh
CMD "./docker/entrypoint.sh"

# # Production image, copy all the files and run next
# FROM base AS production
# ARG PROJECT_NAME_FOLDER
# ARG TOP_FOLDER
# ARG APP_NAME
# ARG APP_FOLDER

# WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

# ENV NODE_ENV production
# # Uncomment the following line in case you want to disable telemetry during runtime.
# # ENV NEXT_TELEMETRY_DISABLED 1

# RUN addgroup --system --gid 1001 nodejs
# RUN adduser --system --uid 1001 nextjs

# COPY --from=builder /${TOP_FOLDER}/${APP_FOLDER}/public ./public

# # Set the correct permission for prerender cache
# RUN mkdir .next
# RUN chown nextjs:nodejs .next

# # Automatically leverage output traces to reduce image size
# # https://nextjs.org/docs/advanced-features/output-file-tracing
# COPY --from=builder --chown=nextjs:nodejs /${TOP_FOLDER}/${APP_FOLDER}/.next/standalone ./
# COPY --from=builder --chown=nextjs:nodejs /${TOP_FOLDER}/${APP_FOLDER}/.next/static ./.next/static

# USER nextjs

# EXPOSE 3000

# ENV PORT 3000

# # server.js is created by next build from the standalone output
# # https://nextjs.org/docs/pages/api-reference/next-config-js/output
# CMD HOSTNAME="0.0.0.0" node server.js