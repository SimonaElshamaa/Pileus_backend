import redis.asyncio as redis
from app.db.redis.config import settings

redis_client: redis.Redis | None = None

async def init_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,  # so you get strings not bytes
        )
        # verify connection at startup
        await redis_client.ping()
    return redis_client

async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None