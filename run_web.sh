#!/bin/sh

bower install --allow-root
python manage.py collectstatic --noinput
python manage.py migrate
su -m probruser -c "uwsgi --socket :8000 --module probr.wsgi_django:application --enable-threads"
