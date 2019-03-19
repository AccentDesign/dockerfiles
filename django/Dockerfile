# build a base image thats needed for all environments

FROM        python:3.6-alpine as base

RUN         set -ex \
            && apk update \
            && apk add --no-cache \
                libpq \
                postgresql-client \
                jpeg-dev \
                zlib-dev \
                make \
                supervisor

# install package requirements into a copy of the base image
# this will include a butt load of cache

FROM        base as builder

ARG         REQUIREMENTS_FILE=/requirements/base.txt

RUN         mkdir /install

WORKDIR     /install

COPY        requirements /requirements

RUN         set -ex \
            && apk update \
            && apk add --no-cache --virtual .build-deps \
                build-base \
                gcc \
                git \
                libc-dev \
                linux-headers \
                musl-dev \
                postgresql-dev \
                python3-dev \
            && PYTHONUSERBASE=/install pip install --user --no-warn-script-location -r $REQUIREMENTS_FILE \
            && apk del .build-deps

# get a fresh copy of the base image and copy in packages without all the cache

FROM        base

COPY        --from=builder /install /usr/local

COPY        ./src /app

COPY        docker-entrypoint.sh /docker-entrypoint.sh
COPY        supervisord.conf /supervisord.conf

WORKDIR     /app

# Django configuration:

ENV         PYTHONUNBUFFERED=1 \
            DJANGO_SETTINGS_MODULE=app.settings \
            SECRET_KEY='***** change me *****' \
            ALLOWED_HOSTS=* \
            RDS_HOSTNAME=db \
            RDS_PORT=5432 \
            RDS_DB_NAME=postgres \
            RDS_USERNAME=postgres \
            RDS_PASSWORD=password \
            EMAIL_HOST=mail \
            EMAIL_PORT=1025 \
            EMAIL_HOST_USER=user \
            EMAIL_HOST_PASSWORD=password

# Django entrypoint:

ENV         DJANGO_MANAGEPY_MIGRATE=on \
            DJANGO_MANAGEPY_COLLECTSTATIC=on

EXPOSE      8000

ENTRYPOINT  ["/docker-entrypoint.sh"]

CMD         ["supervisord", "-c", "/supervisord.conf"]
