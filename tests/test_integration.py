"""
===============================================================================
TEST MODULE C: Integration Tests (test_integration.py)
Phase: 5 (write after main.py is wired up)
===============================================================================

These tests use FastAPI's TestClient to test the full request flow:
    HTTP Request → Middleware → Rate Limiter → Token Bucket → Redis
===============================================================================
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create a fresh FastAPI app for each test.                      │
    │                                                                        │
    │  HINT: return create_app()                                             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_endpoint(app):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: GET /health should return 200 with health status.             │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Create AsyncClient with ASGI transport                           │
    │    2. GET /health                                                      │
    │    3. Assert status_code == 200                                        │
    │    4. Assert response JSON has "status" field                          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_rate_limited_endpoint_returns_headers(app):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Requests to /api/resource should include rate-limit headers.   │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. GET /api/resource with X-API-Key header                          │
    │    2. Assert status_code == 200                                        │
    │    3. Assert "X-RateLimit-Limit" in response headers                   │
    │    4. Assert "X-RateLimit-Remaining" in response headers               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_rate_limit_enforcement(app):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: After exceeding rate limit, requests should return 429.        │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Configure a very low limit for a test client (e.g., 3 requests) │
    │    2. Send 3 requests → all should be 200                              │
    │    3. Send 4th request → should be 429 with Retry-After header        │
    │    4. Assert response body has "error": "Rate limit exceeded"         │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@pytest.mark.asyncio
async def test_admin_crud_operations(app):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TEST: Admin endpoints should support full CRUD on client configs.    │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. POST /admin/clients → create config → assert 200                │
    │    2. GET /admin/clients/client-id → verify created → assert 200     │
    │    3. GET /admin/clients → list all → assert client appears           │
    │    4. DELETE /admin/clients/client-id → assert 200                    │
    │    5. DELETE again → assert 404                                        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
