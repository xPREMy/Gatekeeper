import redis.asyncio as aioredis
from typing import Optional
from app.config import get_settings

settings =get_settings()

class RedisClient:
    """
    Manages an async Redis connection with pool support.
    """
    def __init__(self):

        self._client : Optional[aioredis.Redis] =None
        self._pool : Optional[aioredis.ConnectionPool] =None

    async def connect(self, host: str, port: int, db: int, password: Optional[str] = None) -> None:

        self._pool=aioredis.ConnectionPool.from_url(settings.REDIS_URL,max_connections=20,decode_responses=True)
        self._client = aioredis.Redis(connection_pool=self._pool)

        try:
            await self._client.ping()
        except Exception:
            raise ConnectionError("Failed to connect with Redis Server")

    async def disconnect(self) -> None:

        await self._client.close()
        await self._pool.disconnect()

    def get_client(self) -> aioredis.Redis:

        if self._client is None:
            raise ConnectionError("Redis client not connected. Call connect() first.")
        return self._client

    async def is_healthy(self) -> bool:

        if self._client is None:
            return False
        
        try:
            await self._client.ping()
            return True
        except Exception:
            return False

redis_client = RedisClient()  
