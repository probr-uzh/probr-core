#!/bin/sh

su -m probruser -c "celery -A probr worker -l debug"