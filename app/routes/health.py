"""
===============================================================================
MODULE 9: Health Check Route (health.py)
Difficulty: ★☆☆☆☆ (Easy)
Phase: 4
===============================================================================

PROBLEM STATEMENT:
    Create a /health endpoint that reports the service's health status,
    including whether Redis is reachable. Essential for Docker health
    checks and monitoring.

CONCEPTS:
    - FastAPI APIRouter
    - Dependency injection
    - Health check patterns
===============================================================================
"""

from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.redis_client import redis_client
from app.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Return the health status of the service.                       │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Check Redis health:                                              │
    │       redis_ok = await redis_client.is_healthy()                       │
    │    2. Get settings for version info:                                   │
    │       settings = get_settings()                                        │
    │    3. Determine overall status:                                        │
    │       - "healthy" if redis_ok is True                                  │
    │       - "unhealthy" if redis_ok is False                               │
    │    4. Return HealthResponse(                                           │
    │           status=status,                                               │
    │           redis_connected=redis_ok,                                    │
    │           version=settings.app_version)                                │
    │                                                                        │
    │  INPUT:  None (no parameters)                                          │
    │  OUTPUT: HealthResponse                                                │
    │                                                                        │
    │  EXAMPLE RESPONSE:                                                     │
    │    GET /health                                                         │
    │    200 OK                                                              │
    │    {"status": "healthy", "redis_connected": true, "version": "1.0.0"}  │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
