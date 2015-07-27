#!/usr/bin/env bash
open_browser=false
flush_data=false
host=0.0.0.0:8000
#host=`ipconfig getifaddr en2`:8080


if [ "$flush_data" = true ]; then
	python manage.py flush --noinput
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi
if [ "$open_browser" = true ]; then
	bash -c "sleep 2 && open http://$host/admin" &
fi
python manage.py runserver $host
