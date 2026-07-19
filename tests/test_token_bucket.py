"""
===============================================================================
TEST MODULE A: Token Bucket Tests (test_token_bucket.py)
Phase: 2 (write alongside token_bucket.py)
===============================================================================

These tests verify the Token Bucket algorithm works correctly.
Write these tests AS you build token_bucket.py — TDD style.

SETUP:
    You'll need a running Redis instance for these tests.
    Use pytest-asyncio for async test support.

    pip install pytest pytest-asyncio

    Run: pytest tests/ -v
===============================================================================
"""

import pytest
import pytest_asyncio
import time
import redis.asyncio as aioredis
from app.core.token_bucket import TokenBucket


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def redis_client():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create a Redis client for testing.                             │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Connect to Redis (localhost:6379, db=1 for test isolation)        │
    │    2. yield the client                                                 │
    │    3. After test: flush db 1 and close                                 │
    │       await client.flushdb()                                           │
    │       await client.close()                                             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest_asyncio.fixture
async def token_bucket(redis_client):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create a TokenBucket instance using the test Redis client.     │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_first_request_allowed(token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: First request for a new client should always be allowed.       │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Call: allowed, remaining = await token_bucket.consume(           │
    │           "test-client", max_tokens=10, window_seconds=60)             │
    │    2. Assert: allowed is True                                          │
    │    3. Assert: remaining == 9.0 (started with 10, consumed 1)           │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_bucket_exhaustion(token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: After max_tokens requests, the next should be denied.          │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Set max_tokens = 5                                               │
    │    2. Loop 5 times: consume — all should be allowed                    │
    │    3. Consume once more — should be DENIED with remaining ≈ 0          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_token_refill(token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Tokens should refill over time.                                │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Set max_tokens=2, window_seconds=2 (refill rate = 1 token/sec)  │
    │    2. Consume 2 tokens (exhaust bucket)                                │
    │    3. Immediately try → should be denied                               │
    │    4. Wait 1.5 seconds (asyncio.sleep)                                 │
    │    5. Try again → should be allowed (at least 1 token refilled)       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_different_clients_independent(token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Different client IDs should have independent buckets.          │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Exhaust bucket for "client-A" (max_tokens=2)                    │
    │    2. "client-A" should be denied                                      │
    │    3. "client-B" with same params should be ALLOWED (separate bucket)  │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_tokens_dont_exceed_max(token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Even after a long wait, tokens should cap at max_tokens.       │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Consume 1 token (max_tokens=5, window=60)                       │
    │    2. Wait 2 seconds                                                   │
    │    3. Consume again → remaining should be ≤ 4 (never > max - 1)       │
    │       (Actually it depends on refill rate, but never > max_tokens)     │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
