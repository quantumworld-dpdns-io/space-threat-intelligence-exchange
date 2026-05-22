from __future__ import annotations

from typing import Optional

import redis.asyncio as redis

from stie.config.settings import settings

redis_client: Optional[redis.Redis] = None


async def init_redis():
    global redis_client
    redis_client = redis.from_url(
        settings.redis_url,
        password=settings.redis_password or None,
        decode_responses=True,
    )
    await redis_client.ping()


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client = None


async def get_redis() -> redis.Redis:
    if redis_client is None:
        raise RuntimeError("Redis not initialized")
    return redis_client
