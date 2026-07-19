"""
===============================================================================
MODULE 5: Rate Limiter Service (rate_limiter.py)
Difficulty: ★★★☆☆ (Medium)
Phase: 3
===============================================================================

PROBLEM STATEMENT:
    Build the service layer that sits between the API middleware and the
    token bucket algorithm. It manages per-client configurations stored
    in Redis and delegates rate-limit checks to TokenBucket.

    Think of it as:
        Middleware → RateLimiterService → TokenBucket → Redis

CONCEPTS:
    - Service layer pattern
    - Per-client configuration storage in Redis (as JSON)
    - Fallback to default limits
===============================================================================
"""

import json
from typing import Optional, Dict, List
from app.core.token_bucket import TokenBucket
from app.core.redis_client import redis_client
from app.models.schemas import ClientRateLimitConfig, RateLimitResponse, RateLimitStatus
from app.config import get_settings


class RateLimiterService:
    """
    High-level rate-limiting service with per-client config management.
    """

    def __init__(self, token_bucket: TokenBucket):
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Store the token_bucket and get settings.                    │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. self._bucket = token_bucket                                  │
        │    2. self._settings = get_settings()                              │
        │    3. self._config_prefix = "client_config:"                       │
        │       (Redis key prefix for client configs)                        │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def set_client_config(self, config: ClientRateLimitConfig) -> None:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Store a client's rate-limit configuration in Redis.         │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Build key: f"{self._config_prefix}{config.client_id}"        │
        │    2. Serialize config to JSON: config.model_dump_json()           │
        │    3. Store in Redis: await redis.set(key, json_str)               │
        │                                                                    │
        │  INPUT:  ClientRateLimitConfig                                     │
        │  OUTPUT: None                                                      │
        │                                                                    │
        │  EXAMPLE:                                                          │
        │    await service.set_client_config(                                │
        │        ClientRateLimitConfig(client_id="svc-a",                    │
        │                              max_requests=50,                      │
        │                              window_seconds=30))                   │
        │    # Now "client_config:svc-a" exists in Redis with JSON value     │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def get_client_config(self, client_id: str) -> ClientRateLimitConfig:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Retrieve a client's config from Redis, or return defaults.  │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Build key: f"{self._config_prefix}{client_id}"               │
        │    2. Get from Redis: data = await redis.get(key)                  │
        │    3. If data exists → parse JSON → return ClientRateLimitConfig   │
        │    4. If data is None → return a default config using:             │
        │       ClientRateLimitConfig(                                       │
        │           client_id=client_id,                                     │
        │           max_requests=self._settings.default_rate_limit,          │
        │           window_seconds=self._settings.default_window_seconds)    │
        │                                                                    │
        │  INPUT:  client_id (str)                                           │
        │  OUTPUT: ClientRateLimitConfig (from Redis or defaults)            │
        │                                                                    │
        │  EXAMPLE:                                                          │
        │    config = await service.get_client_config("unknown-client")      │
        │    >>> ClientRateLimitConfig(client_id="unknown-client",           │
        │            max_requests=100, window_seconds=60)  # defaults        │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def delete_client_config(self, client_id: str) -> bool:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Remove a client's config from Redis.                        │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Build key: f"{self._config_prefix}{client_id}"               │
        │    2. Delete: result = await redis.delete(key)                     │
        │    3. Return True if deleted (result > 0), False if key not found  │
        │                                                                    │
        │  INPUT:  client_id (str)                                           │
        │  OUTPUT: bool — True if config existed and was deleted             │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def list_client_configs(self) -> List[ClientRateLimitConfig]:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: List all stored client configurations.                      │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Scan for keys matching f"{self._config_prefix}*"             │
        │       Use: async for key in redis.scan_iter(match=pattern)         │
        │    2. For each key: GET the JSON, parse into ClientRateLimitConfig │
        │    3. Return list of all configs                                   │
        │                                                                    │
        │  INPUT:  None                                                      │
        │  OUTPUT: List[ClientRateLimitConfig]                               │
        │                                                                    │
        │  EDGE CASE: No configs stored → return empty list []               │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def check_rate_limit(self, client_id: str) -> RateLimitResponse:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: The main method — check if a client's request is allowed.   │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Get client config: config = await self.get_client_config(    │
        │           client_id)                                               │
        │    2. Call token bucket: allowed, remaining = await                │
        │           self._bucket.consume(                                    │
        │               client_id, config.max_requests,                      │
        │               config.window_seconds)                               │
        │    3. Build response:                                              │
        │       - If allowed:                                                │
        │           RateLimitResponse(status=ALLOWED, client_id=...,         │
        │               remaining=int(remaining), limit=config.max_requests, │
        │               retry_after=None)                                    │
        │       - If denied:                                                 │
        │           Calculate retry_after:                                   │
        │             refill_rate = config.max_requests/config.window_seconds │
        │             retry_after = (1 - remaining) / refill_rate            │
        │           RateLimitResponse(status=DENIED, ...)                    │
        │    4. Return the RateLimitResponse                                 │
        │                                                                    │
        │  INPUT:  client_id (str)                                           │
        │  OUTPUT: RateLimitResponse                                         │
        │                                                                    │
        │  EXAMPLE:                                                          │
        │    resp = await service.check_rate_limit("svc-a")                  │
        │    >>> RateLimitResponse(status="allowed", client_id="svc-a",      │
        │            remaining=99, limit=100, retry_after=None)              │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE
