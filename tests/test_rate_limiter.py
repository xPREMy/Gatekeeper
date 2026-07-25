import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from app.core.rate_limiter import RateLimiterService
from app.models.schemas import ClientRateLimitConfig, RateLimitStatus
from app.core.redis_client import RedisClient
from app.core.token_bucket import TokenBucket
from app.config import get_settings

settings = get_settings()

# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_token_bucket():
    bucket = MagicMock()
    bucket.consume = AsyncMock(return_value=(True, 99.0))

    redis = MagicMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=1)
    bucket.redis = redis
    
    return bucket
@pytest_asyncio.fixture
async def redis_client():
    redis_client = RedisClient()
    await redis_client.connect()

    try:
        yield redis_client
    finally :
        redis = redis_client.get_client()
        await redis.flushdb()
        await redis_client.disconnect()

@pytest_asyncio.fixture
async def token_bucket(redis_client : RedisClient):
    bucket = TokenBucket(redis_client.get_client())
    return bucket
# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_check_rate_limit_allowed(mock_token_bucket):
    rate_limit_service = RateLimiterService(mock_token_bucket)
    response = await rate_limit_service.check_rate_limit("test_client")
    assert response.status == RateLimitStatus.ALLOWED
    assert response.remaining == 99

@pytest.mark.asyncio
async def test_check_rate_limit_denied(mock_token_bucket):
    mock_token_bucket.consume = AsyncMock(return_value = (False,0.0))
    rate_limit_service = RateLimiterService(mock_token_bucket)
    response = await rate_limit_service.check_rate_limit("test_client")
    assert response.status == RateLimitStatus.DENIED
    assert response.remaining == 0
    assert response.retry_after is not None and response.retry_after > 0


@pytest.mark.asyncio
async def test_set_and_get_client_config(token_bucket : TokenBucket):
    rate_limit_service = RateLimiterService(token_bucket)
    config = ClientRateLimitConfig(
        client_id="test_client",
        max_requests=50,
        window_seconds=60
    )
    await rate_limit_service.set_client_config(config=config)
    config_verify = await rate_limit_service.get_client_config("test_client")
    assert config_verify.max_requests == 50
    assert config_verify.window_seconds == 60
    

@pytest.mark.asyncio
async def test_default_config_for_unknown_client(token_bucket : TokenBucket):
    rate_limit_service = RateLimiterService(token_bucket)
    config =await rate_limit_service.get_client_config("never_configured_client")
    assert config.max_requests == settings.DEFAULT_RATE_LIMIT
    assert config.window_seconds == settings.DEFAULT_WINDOW_SECONDS
