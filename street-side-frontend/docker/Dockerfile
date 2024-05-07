ARG PROJECT_NAME_FOLDER=street-side
ARG TOP_FOLDER=/opt/${PROJECT_NAME_FOLDER}
ARG APP_FOLDER=street-side-frontend
ARG APP_NAME=street_side_api
ARG NODE_VERSION=21

FROM node:${NODE_VERSION}-bookworm-slim AS base

# Rebuild the source code only when needed
FROM base AS builder
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

COPY ${APP_FOLDER}/.eslintrc.json ./
COPY ${APP_FOLDER}/next.config.mjs ./
COPY ${APP_FOLDER}/package-lock.json ./
COPY ${APP_FOLDER}/package.json ./
COPY ${APP_FOLDER}/postcss.config.js ./
COPY ${APP_FOLDER}/README.md ./
COPY ${APP_FOLDER}/tailwind.config.ts ./
COPY ${APP_FOLDER}/tsconfig.json ./
COPY ${APP_FOLDER}/.env.local ./

RUN npm install;

# Dev image, copy all the files and run next
FROM builder AS development
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${APP_FOLDER}/docker/docker_entrypoint.sh docker/entrypoint.sh
CMD "./docker/entrypoint.sh"

# Dev image, copy all the files and run next
FROM builder AS production
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${APP_FOLDER}/app app
COPY ${APP_FOLDER}/api api
RUN npm run build

EXPOSE 3000

ENTRYPOINT [ "npm", "run", "start" ]