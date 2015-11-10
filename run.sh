#!/usr/bin/env bash

open_browser=false
host=0.0.0.0:8000

if [ "$open_browser" = true ]; then
	bash -c "sleep 2 && open http://$host/admin" &
fi

python manage.py runserver $host
