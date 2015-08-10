#!/bin/sh

bower install --allow-root
python manage.py collectstatic --noinput
python manage.py migrate
uwsgi --socket :8000 --module probr.wsgi_django:application --enable-threads
