from nest.core import Injectable

from fastapi import HTTPException

import redis
from src.orm_config import REDIS_CONFIG
from src.redis.redis_model import RedisInput


@Injectable
class RedisService:
    def __init__(self):
        self.redis_client = redis.StrictRedis(**REDIS_CONFIG)

    def set(self, redis_input: RedisInput):
        if self.exists(redis_input.key):
            raise HTTPException(status_code=400, detail="Key already exists")
        self.redis_client.set(redis_input.key, redis_input.value)

    def get(self, redis_key: str):
        return self.redis_client.get(redis_key)

    def exists(self, redis_key: str):
        return self.redis_client.exists(redis_key)

    def delete(self, redis_key: str):
        self.redis_client.delete(redis_key)
