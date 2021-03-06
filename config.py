import os

# qconn = q.q(host = 'localhost', port = 8083, user = 'sunqi')
# Q_HOST = os.environ.get('Q_HOST_ADDR','localhost')
Q_HOST = os.environ.get('Q_HOST_ADDR','39.105.55.115')
Q_PORT = os.environ.get('Q_PORT', 9005)
Q_USER= os.environ.get('Q_USER', 'sunqi')


WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL', "ws://47.75.208.12:8090/")
FULL_WEBSOCKET_URL = os.environ.get('FULL_WEBSOCKET_URL', "ws://47.75.208.12:8090/")

ES_WRAPPER = os.environ.get('ES_WRAPPER', "http://95.216.32.252:5000") # clockwork
# MONGODB_DB_URL = os.environ.get('MONGO_WRAPPER', "mongodb://monitor:ka649Ndhy10&@47.91.216.172:27017/cybex") # clockwork
MONGODB_DB_URL = os.environ.get('MONGO_WRAPPER', "mongodb://yoyo:yoyo123@127.0.0.1:27017/cybex") # clockwork
# MONGODB_DB_NAME = os.environ.get('MONGO_DB_NAME', 'cybex')
MONGODB_DB_NAME = os.environ.get('MONGO_DB_NAME', 'cybex')

# Database connection: see https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS
# Cache: see https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
CACHE = {
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'simple'),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 600)) # 10 min
}

# Configure profiler: see https://github.com/muatik/flask-profiler
PROFILER = {
    'enabled': os.environ.get('PROFILER_ENABLED', False),
    'username': os.environ.get('PROFILER_USERNAME', None),
    'password': os.environ.get('PROFILER_PASSWORD', None),
}

Port=9092
