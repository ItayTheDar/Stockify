from nest.core import Controller, Get, Post, Delete

from src.redis.redis_model import Redis, RedisInput, RedisKey
from src.redis.redis_service import RedisService


@Controller("redis")
class RedisController:

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    @Get("/{key}")
    def get(self, key: str):
        return self.redis_service.get(key)

    @Post("/")
    def set(self, redis_input: RedisInput):
        return self.redis_service.set(redis_input)

    @Delete("/{key}")
    def delete(self, key: str):
        return self.redis_service.delete(key)

    @Get("/exists/{key}")
    def exists(self, key: str):
        return self.redis_service.exists(key)
