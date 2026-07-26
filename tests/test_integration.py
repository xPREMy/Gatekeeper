"""
===============================================================================
TEST MODULE C: Integration Tests (test_integration.py)
Phase: 5 (write after main.py is wired up)
===============================================================================

These tests use FastAPI's TestClient to test the full request flow:
    HTTP Request → Middleware → Rate Limiter → Token Bucket → Redis
===============================================================================
"""

import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import create_app

@pytest_asyncio.fixture
async def app():
    app = create_app()

    async with LifespanManager(app):
        yield app

@pytest.mark.asyncio
async def test_health_endpoint(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client :
        response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("healthy","unhealthy")
    assert "redis_connected" in  body

@pytest.mark.asyncio
async def test_rate_limited_endpoint_returns_headers(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client :
        response = await client.get("/api/resource",headers={"X-API-Key": "test-client"})

    assert response.status_code == 200
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers


@pytest.mark.asyncio
async def test_rate_limit_enforcement(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response_set = await client.post(
            "/admin/clients" , 
            json={
                "client_id": "test-client",
                "max_requests": 3,
                "window_seconds": 300
            },
        )
        response1 = await client.get("/api/resource",headers={"X-API-Key": "test-client"})
        response2 = await client.get("/api/resource",headers={"X-API-Key": "test-client"})
        response3 = await client.get("/api/resource",headers={"X-API-Key": "test-client"})
        response4 = await client.get("/api/resource",headers={"X-API-Key": "test-client"})

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert response4.status_code == 429
    assert response4.json()["error"] == "Rate limit exceeded"

@pytest.mark.asyncio
async def test_admin_crud_operations(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client :
        response_set = await client.post(
            "/admin/clients",
            json={
                "client_id" : "test_client",
                "max_requests" : 80,
                "window_seconds" : 50
            }
        )
        response_get = await client.get("/admin/clients/test_client")
        response_get_all = await client.get("/admin/clients")
        response_delete1 = await client.delete("/admin/clients/test_client")
        response_delete2 = await client.delete("/admin/clients/test_client")

    assert response_set.status_code == 200
    assert response_set.json()["data"]["client_id"] == "test_client"

    assert response_get.status_code == 200
    assert response_get.json()["client_id"] == "test_client"
    
    assert response_get_all.status_code == 200
    print(response_get_all.json())
    assert response_delete1.status_code == 200
    assert response_delete2.status_code == 404