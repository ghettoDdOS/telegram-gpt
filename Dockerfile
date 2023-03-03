FROM python:3.11-alpine

WORKDIR /var/www/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install global packages
RUN apk update \
    && apk upgrade \
    && apk add --no-cache  \
    curl \
    bash

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH="${PATH}:/etc/poetry/bin"

# install backend packages
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN set -ex && poetry install --no-root

COPY . .

ENTRYPOINT [ "poetry", "run", "start" ]
