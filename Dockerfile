FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
## prevents python from writing pyc files to dics
ENV PYTHONDONTWRITEBYTECODE 1
## prevents python from bufferin stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        python-dev \
        libxml2 \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev \
        libxml2-dev && \
    apk add libxslt-dev

RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile.lock /app/Pipfile.lock
COPY Pipfile /app/Pipfile
RUN pipenv lock --requirements > requirements.txt
RUN CFLAGS="-O0" pip install -r requirements.txt

# copy project
ADD src /app/src
COPY ./src/ /app/src
COPY .env /app
COPY manage_db.py /app
COPY Pipfile /app
COPY Pipfile.lock /app
COPY config.cfg /app
COPY main.py /app
