FROM docker.io/postgis/postgis:16-3.4-alpine
RUN apk update
RUN apk upgrade
RUN apk add --no-cache bash

EXPOSE ${PORT_DATABASE}