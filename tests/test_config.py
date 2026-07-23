# from app.config import get_settings
# s = get_settings()
# print(s.REDIS_HOST)  

# from app.models.schemas import ClientRateLimitConfig
# c = ClientRateLimitConfig(client_id="test", max_requests=50, window_seconds=30)
# print(c.model_dump_json())

from app.config import get_settings
from app.core.redis_client import RedisClient
from app.core import token_bucket
import asyncio

async def main():
    client = RedisClient()

    await client.connect()

    print(await client.is_healthy())
    await client.disconnect()
    print( await client.is_healthy())

asyncio.run(main())