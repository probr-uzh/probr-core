#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
uwsgi --socket :8001 --module probr.wsgi_django:application --processes 4 --master --enable-threads
