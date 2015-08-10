#!/bin/sh

uwsgi --socket :8001 --module probr.wsgi_websocket:application --enable-threads
