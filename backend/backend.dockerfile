FROM docker.io/python:3.12-rc-alpine

RUN apk update
RUN apk upgrade

WORKDIR /app

# Packages
RUN apk add --no-cache \
## terminal
bash \
## Install python
py3-pip python3 \
## To Build python packages
gcc g++ python3-dev \
## To build uvloop
libffi-dev build-base \
## Install Poetry (python package manager)
curl \
## Database tools
mysql mysql-client \
## Others
libxml2-dev libxslt-dev \
rust cargo openssl-dev postgresql-dev 

ENV POETRY_HOME=/opt/poetry
###RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/usr/local/bin:/opt/poetry/bin"
RUN pip install poetry

# Run poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install

# magic trick to execute fastApi
#CMD ["poetry", "run", "uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8888", "--loop", "uvloop", "--log-level", "info", "backend.api:app"]
#CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8888"]

EXPOSE ${PORT_BACKEND}