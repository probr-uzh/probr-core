__author__ = 'ale'

import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "probr.settings")

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()