#!/usr/bin/env bash

# fail on first error
set -e
echo "> Running start script..."

echo "> Wait for database on $DATABASE_SERVER to be ready..."

[ ! -z "$DATABASE_SERVER" ] && $WORKDIR/sh/wait-for-it.sh $DATABASE_SERVER:5432 --timeout=120

echo "> database seems to be ready..."

echo "> Upgrading database model..."

cd $WORKDIR

python manage.py db upgrade

echo "> Upgrade successful"

echo "> Starting backend ..."

gunicorn --bin 0.0.0.0:$PORT main:app
