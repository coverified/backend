FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
## prevents python from writing pyc files to dics
ENV PYTHONDONTWRITEBYTECODE 1
## prevents python from bufferin stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add --update --upgrade --no-cache --virtual .build-deps \
        bash \
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

# copy startup scripts
COPY ./sh/backend-container-startup.sh /
COPY ./sh/wait-for-it.sh /

# make startup scripts executable
RUN ["chmod", "+x", "/backend-container-startup.sh"]
RUN ["chmod", "+x", "/wait-for-it.sh"]

# copy project
ADD src /app/src
COPY ./src/ /app/src
COPY .env /app
COPY manage_db.py /app
COPY Pipfile /app
COPY Pipfile.lock /app
COPY config.cfg /app
COPY main.py /app

# create the app user
RUN addgroup -S app && adduser -S app -G app -h /app

# chown entry scripts to app user
RUN chown -R app:app /backend-container-startup.sh
RUN chown -R app:app /wait-for-it.sh

# change to the app user
USER app

CMD ["/backend-container-startup.sh"]