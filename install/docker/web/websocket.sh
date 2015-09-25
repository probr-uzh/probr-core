#!/bin/sh

uwsgi --socket :8002 --module probr.wsgi_websocket:application --enable-threads
