from base_settings import *

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = [ 'json', ]
MONGO_URI = 'mongodb://localhost/probr_core'

# production database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'probr',
#        'USER': 'probr',
#        'PASSWORD':'blablaz1',
#        'HOST':'127.0.0.1',
#        'PORT':''
#    }
#}
