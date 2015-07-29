#!/usr/bin/env bash

# Usage:
# ./setup
# ./setup flush

action="$1"

if [ "$action" = 'flush' ]; then
	python manage.py flush --noinput
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi

pip install -r requirements.txt
python manage.py migrate
bower install
python manage.py collectstatic --noinput
