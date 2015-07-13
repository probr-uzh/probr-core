#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate
bower install
python manage.py collectstatic --noinput
