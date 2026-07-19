"""
===============================================================================
MODULE 12: Main Application Entry Point (main.py)
Difficulty: ★★★☆☆ (Medium) — THE WIRING MODULE
Phase: 5
===============================================================================

PROBLEM STATEMENT:
    Create the FastAPI application, wire up all components (Redis client,
    token bucket, rate limiter service, middleware, routes), and define
    the startup/shutdown lifecycle events.

    This is where everything comes together.

CONCEPTS:
    - FastAPI application lifecycle (lifespan context manager)
    - Dependency wiring
    - Router inclusion
    - Middleware registration order
===============================================================================
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import get_settings
from app.core.redis_client import redis_client
from app.core.token_bucket import TokenBucket
from app.core.rate_limiter import RateLimiterService
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.routes import health, admin, gateway


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Define the app's startup and shutdown lifecycle.               │
    │                                                                        │
    │  ON STARTUP (before `yield`):                                          │
    │    1. Load settings: settings = get_settings()                         │
    │    2. Connect to Redis:                                                │
    │       await redis_client.connect(                                      │
    │           host=settings.redis_host,                                    │
    │           port=settings.redis_port,                                    │
    │           db=settings.redis_db,                                        │
    │           password=settings.redis_password)                            │
    │    3. Create TokenBucket:                                              │
    │       bucket = TokenBucket(redis_client.get_client())                  │
    │    4. Create RateLimiterService:                                       │
    │       rate_limiter = RateLimiterService(bucket)                        │
    │    5. Store on app.state for access from routes/middleware:            │
    │       app.state.rate_limiter = rate_limiter                            │
    │    6. Print: "🚀 Gatekeeper started — Redis connected"                │
    │                                                                        │
    │  yield  ← app runs here                                               │
    │                                                                        │
    │  ON SHUTDOWN (after `yield`):                                          │
    │    1. Disconnect Redis:                                                │
    │       await redis_client.disconnect()                                  │
    │    2. Print: "🛑 Gatekeeper shutting down"                             │
    │                                                                        │
    │  HINT: Use try/except around startup to handle Redis connection        │
    │        failures gracefully.                                            │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # YOUR CODE HERE
    yield


def create_app() -> FastAPI:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Build and return the fully configured FastAPI application.      │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Create FastAPI instance:                                          │
    │       app = FastAPI(                                                   │
    │           title="Gatekeeper API Gateway",                              │
    │           description="Distributed Rate Limiter & API Gateway",       │
    │           version=get_settings().app_version,                          │
    │           lifespan=lifespan)                                           │
    │                                                                        │
    │    2. Include routers:                                                  │
    │       app.include_router(health.router)                                │
    │       app.include_router(admin.router)                                 │
    │       app.include_router(gateway.router)                               │
    │                                                                        │
    │    3. Return app                                                        │
    │                                                                        │
    │  NOTE ON MIDDLEWARE:                                                    │
    │    The middleware needs the rate_limiter, which is only available       │
    │    after startup. You have two options:                                │
    │    A) Add middleware in the lifespan after creating the rate_limiter   │
    │    B) Make the middleware handle a missing rate_limiter gracefully     │
    │    Think about which approach is cleaner.                              │
    │                                                                        │
    │  OUTPUT: FastAPI — the configured app instance                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TASK: Create the app instance and add the uvicorn runner
# ─────────────────────────────────────────────────────────────────────────────

app = None  # YOUR CODE HERE — replace with create_app()

if __name__ == "__main__":
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Run the app with uvicorn.                                      │
    │                                                                        │
    │    import uvicorn                                                      │
    │    settings = get_settings()                                           │
    │    uvicorn.run(                                                        │
    │        "app.main:app",                                                 │
    │        host=settings.server_host,                                      │
    │        port=settings.server_port,                                      │
    │        reload=settings.debug)                                          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
