ARG PROJECT_NAME_FOLDER=street-side
ARG TOP_FOLDER=/opt/${PROJECT_NAME_FOLDER}
ARG APP_FOLDER=street-side-scrapper
ARG APP_NAME=street_side
ARG PYTHON_VERSION=3.11.3
ARG POETRY_VERSION=1.6.1

#
# Stage: stagting
#
FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim-buster as staging
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

# Adding trusting keys to apt for repositories
RUN apt-get update &&\
    apt-get install -y gnupg &&\
    apt-get install -y wget &&\
    apt-get -y install sudo

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Adding Google Chrome to the repositories
RUN sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'


# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Install project dependencies
WORKDIR ${TOP_FOLDER}/${APP_FOLDER}

RUN apt-get install -yqq unzip && \
    apt install -y curl

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

# Install poetry
RUN apt update && \
    apt install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} POETRY_VERSION=${POETRY_VERSION} python3 -

COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/poetry.lock ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/pyproject.toml ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/README.md  ./
COPY ${PROJECT_NAME_FOLDER}/street-side-data-models ${TOP_FOLDER}/${APP_FOLDER}/../street-side-data-models
COPY ${PROJECT_NAME_FOLDER}/street-side-storage ${TOP_FOLDER}/${APP_FOLDER}/../street-side-storage

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
RUN poetry install

RUN apt-get update\
    && apt-get install -y netcat

COPY ${PROJECT_NAME_FOLDER}/${APP_FOLDER}/docker/dev-entrypoint.sh ${TOP_FOLDER}/${APP_FOLDER}/docker/entrypoint.sh
ENTRYPOINT [ "./docker/entrypoint.sh" ]