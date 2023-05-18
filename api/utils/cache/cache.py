import redis
from flask_caching import Cache

redis_cache = redis.Redis(host='localhost', port=6379, db=0)

cache = Cache(config={'CACHE_TYPE': 'redis',
              'CACHE_REDIS_URL': 'redis://localhost:6379/0'})


def init_cache(app):
    cache.init_app(app)

    with app.app_context():
        redis_cache.ping()
