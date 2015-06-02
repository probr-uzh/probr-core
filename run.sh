#!/usr/bin/env bash
open_browser=true
flush_data=false
host=localhost:8080
#host=`ipconfig getifaddr en2`:8080


if [ "$flush_data" = true ]; then
	python manage.py flush --noinput
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi
if [ "$open_browser" = true ]; then
	bash -c "sleep 2 && open http://$host/admin" &
fi
python manage.py runserver $host
