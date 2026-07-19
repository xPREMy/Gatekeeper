"""
===============================================================================
TEST MODULE B: Rate Limiter Service Tests (test_rate_limiter.py)
Phase: 3 (write alongside rate_limiter.py)
===============================================================================
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from app.core.rate_limiter import RateLimiterService
from app.models.schemas import ClientRateLimitConfig, RateLimitStatus


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_token_bucket():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create a mock TokenBucket for isolated service testing.        │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Create a MagicMock                                               │
    │    2. Set consume as AsyncMock returning (True, 99.0) by default      │
    │    3. Return the mock                                                  │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_check_rate_limit_allowed(mock_token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: check_rate_limit returns ALLOWED when bucket has tokens.       │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Mock consume to return (True, 99.0)                              │
    │    2. Call service.check_rate_limit("test-client")                     │
    │    3. Assert status == RateLimitStatus.ALLOWED                         │
    │    4. Assert remaining == 99                                           │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_check_rate_limit_denied(mock_token_bucket):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: check_rate_limit returns DENIED when bucket is empty.          │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Mock consume to return (False, 0.0)                              │
    │    2. Call service.check_rate_limit("test-client")                     │
    │    3. Assert status == RateLimitStatus.DENIED                          │
    │    4. Assert retry_after is not None and > 0                           │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_set_and_get_client_config():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Can set a client config and retrieve it.                       │
    │                                                                        │
    │  NOTE: This needs a real Redis. Skip if not available.                │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Set config for "test-client" with max_requests=50               │
    │    2. Get config for "test-client"                                     │
    │    3. Assert max_requests == 50                                        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_default_config_for_unknown_client():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Unknown clients should get default config.                     │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get config for "never-configured-client"                         │
    │    2. Assert max_requests == settings.default_rate_limit               │
    │    3. Assert window_seconds == settings.default_window_seconds         │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
