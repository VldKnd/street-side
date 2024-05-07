ARG PROJECT_NAME_FOLDER=street-side
ARG TOP_FOLDER=/opt/${PROJECT_NAME_FOLDER}
ARG APP_FOLDER=street-side-api
ARG APP_NAME=street_side_api
ARG PYTHON_VERSION=3.11.3
ARG POETRY_VERSION=1.6.1

#
# Stage: stagting
#
FROM python:${PYTHON_VERSION}-slim-buster as staging
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

    
# Install project dependencies
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

RUN apt update \
    && apt install -y curl \
    && curl -L https://github.com/golang-migrate/migrate/releases/download/v4.15.1/migrate.linux-amd64.tar.gz | tar xvz

# Install poetry
RUN apt update && \
    apt install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 -

COPY ${APP_FOLDER}/poetry.lock ${APP_FOLDER}/pyproject.toml ${APP_FOLDER}/README.md  ./
COPY street-side-data-models ${TOP_FOLDER}/${APP_FOLDER}/../street-side-data-models
COPY street-side-storage ${TOP_FOLDER}/${APP_FOLDER}/../street-side-storage
RUN poetry install --without dev
COPY ${APP_FOLDER}/database ./database

#
# Stage: worker
#
FROM staging as worker
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER


# Install project in editable mode and with development dependencies
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${APP_FOLDER}/$APP_NAME ./$APP_NAME
RUN poetry install --without dev

RUN apt-get update\
    && apt-get install -y netcat

COPY ${APP_FOLDER}/docker/wait-for.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/wait-for.sh
COPY ${APP_FOLDER}/docker/docker-entrypoint.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/entrypoint.sh
COPY --from=staging ${TOP_FOLDER}/${APP_FOLDER}/migrate ${TOP_FOLDER}/${APP_FOLDER}/docker/migrate

EXPOSE 8080

ENTRYPOINT [ "./docker/entrypoint.sh" ]
