#!/bin/bash
set -e

ROOT_DIR=$(pwd)
MAIN_DIR=/var/www/randomcoffeebot
BACKEND_DIR=/var/www/randomcoffeebot/backend
STATIC_DIR=/var/www/randomcoffeebot/static
rm -r $BACKEND_DIR 2> /dev/null || true
rm -r $STATIC_DIR 2> /dev/null || true
mkdir -p $BACKEND_DIR
mkdir -p $STATIC_DIR

echo copying files to $BACKEND_DIR...
cp -r $ROOT_DIR/* $BACKEND_DIR

echo updating pip packages...
$MAIN_DIR/.env/bin/pip install -r $ROOT_DIR/requirements.txt

echo copying local settings...
cp $MAIN_DIR/local_settings.py $BACKEND_DIR/random_coffee_bot

echo applying database migrations...
$MAIN_DIR/.env/bin/python $BACKEND_DIR/manage.py migrate

echo restarting server...
supervisorctl restart randomcoffeebot