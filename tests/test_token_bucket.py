import pytest
import pytest_asyncio
import time
import redis.asyncio as aioredis
from app.core.token_bucket import TokenBucket
from app.core.redis_client import RedisClient
import asyncio

# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def redis_client():
    client = RedisClient()
    await client.connect()

    try:
        yield client.get_client()
    finally :
        redis_client=client.get_client()
        await redis_client.flushdb()
        await client.disconnect()


@pytest_asyncio.fixture
async def token_bucket(redis_client : RedisClient):
    bucket = TokenBucket(redis_client)
    return bucket


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_first_request_allowed(token_bucket : TokenBucket):
    allowed , remaining = await token_bucket.consume(
        "test_client",10,60
    )
    assert  allowed is True
    assert remaining ==pytest.approx(9.0) , "started with 10 consumed 1"


@pytest.mark.asyncio
async def test_bucket_exhaustion(token_bucket : TokenBucket):
    allowed , remaining = await token_bucket.consume(
        "test_client",1,60,1
    )
    allowed , remaining = await token_bucket.consume(
        "test_client",1,60,1
    )
    assert  allowed is False
    assert remaining == 0 , "started with 1 consumed 1"


@pytest.mark.asyncio
async def test_token_refill(token_bucket : TokenBucket):
    allowed , remaining = await token_bucket.consume(
        "test_client",1,1
    )
    await asyncio.sleep(1.1)
    allowed , remaining = await token_bucket.consume(
        "test_client",1,1
    )
    assert  allowed is True
    assert remaining == 0 , "started with 10 consumed 1"

@pytest.mark.asyncio
async def test_different_clients_independent(token_bucket : TokenBucket):
    all1,rem1 = await token_bucket.consume("Client_A",1,60,1)
    all1,rem1 = await token_bucket.consume("Client_A",1,60,1)
    all2,rem2= await token_bucket.consume("Client_B",1,60,1)
    assert all1 is False
    assert all2 is True
    assert rem1 == 0
    assert rem2 == 0

