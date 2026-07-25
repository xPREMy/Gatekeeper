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
    redis_ok = redis_client.is_healthy()
    settings = get_settings()
    if redis_ok :
        status = "healthy"
    else:
        status = "unhealthy"

    return HealthResponse(
        status=status,
        redis_connected=redis_ok,
        version=settings.APP_VERSION
    )
