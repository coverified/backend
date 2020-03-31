#!/usr/bin/env bash

# fail on first error
set -e
echo "> Running start script..."

echo "> Wait for database on $DATABASE_SERVER to be ready..."

[ ! -z "$DATABASE_SERVER" ] && $WORKDIR/sh/wait-for-it.sh $DATABASE_SERVER:5432 --timeout=120

echo "> database seems to be ready..."

echo "> Migrating database model..."

echo $WORKDIR
echo pwd

cd $WORKDIR
echo pwd

python manage_db.py db init
python manage_db.py db migrate
python manage_db.py db upgrade

echo "> Migration successful"

echo "> Starting backend ..."

python main.py
