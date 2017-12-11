from base_settings import *
import os

DEBUG = os.getenv('DEBUG', True)

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'ws4redis',
    'taggit',
    'taggit_serializer',
    'rest_framework',
    'utils',
    'devices',
    'captures',
    'device_captures',
)

CELERY_ACCEPT_CONTENT = ['json',]

# Compress
COMPRESS_PRECOMPILERS = (
    ('text/less', '/usr/local/bin/lessc {infile} {outfile}'),
)
# production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'postgres')
    }
}

# Redis Connection for Sockets
WS4REDIS_CONNECTION = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', '6379')
}

# Mongo settings
MONGO_URI = os.getenv('MONGO_URL', 'mongodb://localhost/probr_core')

# Celery settings
BROKER_URL = os.getenv('BROKER_URL', 'redis://redis:6379/1')