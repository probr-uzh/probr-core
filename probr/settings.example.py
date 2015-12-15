from base_settings import *

# Redis Connection for Sockets
# WS4REDIS_CONNECTION = {
#     'host': os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'localhost'),
#     'port': os.environ.get('REDIS_PORT_6379_TCP_PORT', '6379'),
# }
# 
# Broker URL for Celery
# BROKER_URL = 'redis://' + os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'localhost') + ':' + os.environ.get('REDIS_PORT_6379_TCP_PORT', '6379');
# CELERY_ACCEPT_CONTENT = [ 'json', ]
# 
# # MongoURI
# MONGO_URI = 'mongodb://' + os.environ.get('MONGODB_PORT_27017_TCP_ADDR', 'localhost') + ':' + os.environ.get('MONGODB_PORT_27017_TCP_PORT', '27017') + '/probr-core';
# 
# # Compress
# COMPRESS_PRECOMPILERS = (
#     ('text/less', 'lessc {infile} {outfile}'),
# )
# 
# production database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'probr',
#         'USER': 'probr',
#         'PASSWORD': 'probr',
#         'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
#         'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', '5432'),
#     }
# }
