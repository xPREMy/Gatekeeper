"""
===============================================================================
MODULE 3: Redis Client Manager (redis_client.py)
Difficulty: ★★☆☆☆ (Easy-Medium)
Phase: 2
===============================================================================

PROBLEM STATEMENT:
    Create a Redis connection manager that handles connecting, disconnecting,
    and health-checking Redis. This is a foundational piece — the rate limiter
    stores ALL its state in Redis so it works across multiple app instances.

CONCEPTS:
    - redis.asyncio (aioredis) for non-blocking Redis
    - Connection pooling
    - Async context management

REFERENCE:
    https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html
===============================================================================
"""

import redis.asyncio as aioredis
from typing import Optional


class RedisClient:
    """
    Manages an async Redis connection with pool support.
    """

    def __init__(self):
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Initialize instance variables.                              │
        │                                                                    │
        │  Set up:                                                           │
        │    self._client : Optional[aioredis.Redis] = None                  │
        │    self._pool   : Optional[aioredis.ConnectionPool] = None         │
        │                                                                    │
        │  Do NOT connect here. Connection happens in connect().             │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def connect(self, host: str, port: int, db: int, password: Optional[str] = None) -> None:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Establish a connection pool and create a Redis client.      │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Create a ConnectionPool using aioredis.ConnectionPool(       │
        │         host=host, port=port, db=db, password=password,            │
        │         decode_responses=True, max_connections=20                  │
        │       )                                                            │
        │    2. Create the client: aioredis.Redis(connection_pool=pool)      │
        │    3. Store both in self._pool and self._client                    │
        │    4. Verify connection with a ping: await self._client.ping()     │
        │                                                                    │
        │  INPUT:  host (str), port (int), db (int), password (Optional)     │
        │  OUTPUT: None — but raises ConnectionError if ping fails           │
        │                                                                    │
        │  EXAMPLE:                                                          │
        │    client = RedisClient()                                          │
        │    await client.connect("localhost", 6379, 0)                      │
        │    # Now client.get_client() returns a usable Redis instance       │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def disconnect(self) -> None:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Gracefully close the Redis connection and pool.             │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. If self._client exists → await self._client.close()          │
        │    2. If self._pool exists   → await self._pool.disconnect()       │
        │    3. Set both to None                                             │
        │                                                                    │
        │  INPUT:  None                                                      │
        │  OUTPUT: None                                                      │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    def get_client(self) -> aioredis.Redis:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Return the active Redis client.                             │
        │                                                                    │
        │  INPUT:  None                                                      │
        │  OUTPUT: aioredis.Redis instance                                   │
        │  RAISES: ConnectionError if self._client is None                   │
        │          (message: "Redis client not connected. Call connect()     │
        │           first.")                                                 │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def is_healthy(self) -> bool:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Check if Redis is alive and responding.                     │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Try: await self._client.ping()                               │
        │    2. Return True if ping succeeds                                 │
        │    3. Catch any exception → return False                           │
        │                                                                    │
        │  INPUT:  None                                                      │
        │  OUTPUT: bool — True if connected and responding, False otherwise  │
        │                                                                    │
        │  EDGE CASES:                                                       │
        │    - self._client is None → return False                           │
        │    - Network timeout → return False                                │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# Module-level singleton
# ─────────────────────────────────────────────────────────────────────────────

# TASK: Create a single module-level instance: redis_client = RedisClient()
# All other modules will import this instance.

redis_client = None  # YOUR CODE HERE — replace None with RedisClient()
