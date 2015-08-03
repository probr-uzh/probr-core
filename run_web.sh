#!/bin/sh

bower install --allow-root
su -m probruser -c "python manage.py collectstatic --noinput"
su -m probruser -c "python manage.py migrate"
su -m probruser -c "uwsgi --socket :8000 --module probr.wsgi:application --enable-threads"
