from base_settings import *

# Broker URL for Celery
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = [ 'json', ]

# MongoURI
MONGO_URI = 'mongodb://localhost/probr_core'

# Compress
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

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
