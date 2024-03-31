FROM docker.io/python:3.12-rc-alpine3.18

RUN apk update
RUN apk upgrade

WORKDIR /app

# Packages
## Install python
RUN apk add py3-pip python3
## To Build python packages
RUN apk add gcc g++ python3-dev
## To build uvloop
RUN apk add libffi-dev build-base
## Install Poetry (python package manager)
RUN apk add curl
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/usr/local/bin:/opt/poetry/bin"
## Other packages
RUN apk add libxml2-dev libxslt-dev
RUN apk add rust cargo openssl-dev postgresql-dev

# Run poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install

# magic trick to execute fastApi
CMD ["poetry", "run", "uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8888", "--loop", "uvloop", "--log-level", "info", "backend.api:app"]

EXPOSE 8888