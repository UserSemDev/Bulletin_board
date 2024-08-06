FROM python:3.11
LABEL authors="UserSemDev"

ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.2 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /code

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /code