#!/bin/sh

uwsgi --socket :8002 --module probr.wsgi_websocket:application --gevent 1000 --http-websockets --workers=2 --master
