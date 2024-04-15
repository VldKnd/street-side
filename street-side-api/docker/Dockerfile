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
ARG PROJECT_NAME_FOLDER
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

# Install poetry
RUN apt update && \
    apt install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 -

# Install project dependencies
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/poetry.lock ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/pyproject.toml ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/README.md  ./
COPY ${PROJECT_NAME_FOLDER}/street-side-data-models ${TOP_FOLDER}/${APP_FOLDER}/../street-side-data-models
COPY ${PROJECT_NAME_FOLDER}/street-side-storage ${TOP_FOLDER}/${APP_FOLDER}/../street-side-storage
RUN poetry install --without dev
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/database ./database

#
# Stage: development
#
FROM staging as development
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER


# Install project in editable mode and with development dependencies
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/$APP_NAME ./$APP_NAME
RUN poetry install --without dev

RUN apt-get update\
    && apt-get install -y netcat

COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/docker/wait-for.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/wait-for.sh
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/docker/dev-entrypoint.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/entrypoint.sh
ENTRYPOINT [ "./docker/entrypoint.sh" ]

#
# Stage: build
#
FROM staging as build
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

WORKDIR ${TOP_FOLDER}/${APP_FOLDER}
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/$APP_NAME ./$APP_NAME
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

#
# Stage: production
#
FROM python:$PYTHON_VERSION-slim-buster as production
ARG PROJECT_NAME_FOLDER
ARG TOP_FOLDER
ARG APP_NAME
ARG APP_FOLDER

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

# Get build artifact wheel and install it respecting dependency versions
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

COPY --from=build ${TOP_FOLDER}/${APP_FOLDER}/dist/*.whl ./
COPY --from=build ${TOP_FOLDER}/${APP_FOLDER}/requirements.txt ./
COPY ${PROJECT_NAME_FOLDER}/street-side-data-models ${TOP_FOLDER}/${APP_FOLDER}/../street-side-data-models
RUN pip install ./$APP_NAME*.whl -r requirements.txt -i https://aws:$(cat /run/secrets/AWS_PYPI_TOKEN)@aqemia-142655614335.d.codeartifact.us-east-1.amazonaws.com/pypi/main/simple
COPY --from=build ${TOP_FOLDER}/${APP_FOLDER}/${APP_NAME}/main.py  ${TOP_FOLDER}/${APP_FOLDER}/${APP_NAME}/main.py
COPY --from=build ${TOP_FOLDER}/${APP_FOLDER}/${APP_NAME}/log_config.json ${TOP_FOLDER}/${APP_FOLDER}/${APP_NAME}/log_config.json
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/docker/prod-entrypoint.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/entrypoint.sh
COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/database ./database

EXPOSE 8080
ENTRYPOINT [ "./docker/entrypoint.sh" ]
