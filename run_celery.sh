#!/bin/sh

su -m probruser -c "celery worker -A probr"