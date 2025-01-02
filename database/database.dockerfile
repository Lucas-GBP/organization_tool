FROM docker.io/postgres:17.2-alpine3.21
RUN apk update
RUN apk upgrade
RUN apk add --no-cache bash

EXPOSE ${PORT_DATABASE}