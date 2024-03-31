FROM docker.io/postgres:16.2-alpine3.18
RUN apk update
RUN apk upgrade
RUN apk add bash