from emitter import Emitter
from probr.base_settings import WS4REDIS_CONNECTION

io=Emitter({'host': WS4REDIS_CONNECTION['host'], 'port': WS4REDIS_CONNECTION['port']})