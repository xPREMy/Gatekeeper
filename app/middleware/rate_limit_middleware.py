"""
===============================================================================
MODULE 8: Rate Limit Middleware (rate_limit_middleware.py)
Difficulty: ★★★☆☆ (Medium)
Phase: 4
===============================================================================

PROBLEM STATEMENT:
    Create a FastAPI middleware that intercepts EVERY incoming request,
    checks the rate limit, and either lets it through (adding rate-limit
    headers) or returns a 429 response.

    Middleware sits between the client and your route handlers:
        Client → Middleware → Route Handler

CONCEPTS:
    - FastAPI / Starlette BaseHTTPMiddleware
    - Request interception
    - Injecting response headers
===============================================================================
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.rate_limiter import RateLimiterService
from app.utils.client_identifier import get_client_identifier
from app.utils.response_builder import build_rate_limit_headers, build_rate_limited_response
from app.models.schemas import RateLimitStatus
from typing import Callable, List


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces rate limits on all incoming requests.
    """

    def __init__(self, app, rate_limiter: RateLimiterService, excluded_paths: List[str] = None):
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Initialize the middleware.                                  │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Call super().__init__(app)                                    │
        │    2. Store self._rate_limiter = rate_limiter                      │
        │    3. Store self._excluded_paths = excluded_paths or ["/health",   │
        │           "/docs", "/openapi.json", "/redoc"]                      │
        │       (These paths should NOT be rate-limited)                     │
        │                                                                    │
        │  INPUT:  app (FastAPI), rate_limiter (RateLimiterService),          │
        │          excluded_paths (optional list of path strings)            │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Intercept the request, check rate limit, decide fate.      │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Check if request.url.path is in self._excluded_paths         │
        │       → If yes: return await call_next(request) immediately        │
        │                                                                    │
        │    2. Extract client ID:                                           │
        │       client_id = get_client_identifier(request)                   │
        │                                                                    │
        │    3. Check rate limit:                                            │
        │       result = await self._rate_limiter.check_rate_limit(client_id)│
        │                                                                    │
        │    4. If result.status == DENIED:                                  │
        │       → return build_rate_limited_response(result)                 │
        │                                                                    │
        │    5. If ALLOWED:                                                  │
        │       → response = await call_next(request)                        │
        │       → Add rate-limit headers to response:                        │
        │         headers = build_rate_limit_headers(result)                  │
        │         for key, value in headers.items():                          │
        │             response.headers[key] = value                          │
        │       → return response                                            │
        │                                                                    │
        │  INPUT:  Request, call_next (handler chain)                         │
        │  OUTPUT: Response (either the actual response + headers, or 429)   │
        │                                                                    │
        │  FLOW DIAGRAM:                                                     │
        │    Request                                                         │
        │      │                                                             │
        │      ▼                                                             │
        │    Is path excluded? ──YES──→ call_next(request)                   │
        │      │ NO                                                          │
        │      ▼                                                             │
        │    Extract client ID                                               │
        │      │                                                             │
        │      ▼                                                             │
        │    Check rate limit                                                │
        │      │                                                             │
        │      ├── DENIED ──→ Return 429 + headers                           │
        │      │                                                             │
        │      └── ALLOWED ─→ call_next(request) + add headers               │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE
