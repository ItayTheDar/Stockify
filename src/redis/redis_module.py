from src.redis.redis_controller import RedisController
from src.redis.redis_service import RedisService
from nest.core import Module


@Module(providers=[RedisService], controllers=[RedisController])
class RedisModule:
    ...
