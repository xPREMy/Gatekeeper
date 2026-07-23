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
        self._bucket = token_bucket
        self._settings = get_settings()
        self._config_prefix = "client_config:" 

    async def set_client_config(self, config: ClientRateLimitConfig) -> None:
        key = f"{self._config_prefix}{config.client_id}"
        config_json = config.model_dump_json()
        redis = redis_client.get_client()
        redis.set(key,config_json)

    async def get_client_config(self, client_id: str) -> ClientRateLimitConfig:
        key= f"{self._config_prefix}{client_id}"
        redis = redis_client.get_client()
        config_json =await redis.get(key)
        if config_json is None:
            return ClientRateLimitConfig(
                client_id=client_id,
                max_requests=self._settings.DEFAULT_RATE_LIMIT,
                window_seconds=self._settings.DEFAULT_WINDOW_SECONDS
            )
        config = ClientRateLimitConfig.model_validate_json(config_json)
        return config

    async def delete_client_config(self, client_id: str) -> bool:
        key = f"{self._config_prefix}{client_id}"
        redis= redis_client.get_client()
        result = await redis.delete(key)
        return result>0

    async def list_client_configs(self) -> List[ClientRateLimitConfig]:
        redis = redis_client.get_client()
        pattern= f"{self._config_prefix}*"
        client_list : List[ClientRateLimitConfig] = []
        async for key in redis.scan_iter(match=pattern):
            config_json = await redis.get(key)
            if config_json is None:
                continue
            config = ClientRateLimitConfig.model_validate_json(config_json)
            client_list.append(config)
        return client_list

    async def check_rate_limit(self, client_id: str) -> RateLimitResponse:
        config = await self.get_client_config(client_id=client_id)
        limit = config.max_requests
        window_seconds = config.window_seconds
        tokens_to_consume=self._settings.Tokens_consume_per_request
        allowed , remaining = await self._bucket.consume(client_id=client_id,max_tokens=limit,window_seconds=window_seconds,tokens_to_consume=tokens_to_consume)
        remaining=remaining
        if allowed :
            return RateLimitResponse(
                status=RateLimitStatus.ALLOWED,
                Client_id=client_id,
                limit=limit,
                remaining=int(remaining),
                retry_after=None
            )
        else :
            refill_rate = limit/window_seconds
            retry_after = (tokens_to_consume - remaining)/refill_rate
            return RateLimitResponse(
                status=RateLimitStatus.DENIED,
                Client_id=client_id,
                limit=limit,
                remaining= 0,
                retry_after=retry_after
            )
