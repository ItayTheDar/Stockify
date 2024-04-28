from typing import Any

from pydantic import BaseModel


class Redis(BaseModel):
    name: str


class RedisInput(BaseModel):
    key: str
    value: Any


class RedisKey(BaseModel):
    key: str
