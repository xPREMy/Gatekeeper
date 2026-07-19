"""
===============================================================================
MODULE 7: Response Builder Utility (response_builder.py)
Difficulty: ★☆☆☆☆ (Easy)
Phase: 3
===============================================================================

PROBLEM STATEMENT:
    Build helper functions that create standardized HTTP responses with
    proper rate-limit headers. These headers tell clients their limits
    and when they can retry.

CONCEPTS:
    - Standard rate-limit HTTP headers (RFCs / conventions)
    - JSONResponse from FastAPI
===============================================================================
"""

from fastapi.responses import JSONResponse
from app.models.schemas import RateLimitResponse, RateLimitStatus


def build_rate_limit_headers(rate_limit_result: RateLimitResponse) -> dict:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Build a dict of standard rate-limit HTTP headers.              │
    │                                                                        │
    │  HEADERS TO INCLUDE:                                                   │
    │    "X-RateLimit-Limit"     → str(rate_limit_result.limit)              │
    │    "X-RateLimit-Remaining" → str(rate_limit_result.remaining)          │
    │                                                                        │
    │    If retry_after is not None:                                          │
    │      "Retry-After"         → str(int(retry_after))                     │
    │      "X-RateLimit-Reset"   → str(int(retry_after))                     │
    │                                                                        │
    │  INPUT:  RateLimitResponse                                             │
    │  OUTPUT: dict[str, str] — header name → value                          │
    │                                                                        │
    │  EXAMPLE (allowed):                                                    │
    │    >>> build_rate_limit_headers(allowed_response)                       │
    │    {"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": "99"}         │
    │                                                                        │
    │  EXAMPLE (denied):                                                     │
    │    >>> build_rate_limit_headers(denied_response)                        │
    │    {"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": "0",          │
    │     "Retry-After": "12", "X-RateLimit-Reset": "12"}                    │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


def build_rate_limited_response(rate_limit_result: RateLimitResponse) -> JSONResponse:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Build a 429 Too Many Requests response for denied requests.    │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get headers from build_rate_limit_headers(rate_limit_result)     │
    │    2. Build body: {                                                    │
    │           "error": "Rate limit exceeded",                              │
    │           "client_id": rate_limit_result.client_id,                    │
    │           "retry_after": rate_limit_result.retry_after                 │
    │       }                                                                │
    │    3. Return JSONResponse(status_code=429, content=body, headers=hdrs) │
    │                                                                        │
    │  INPUT:  RateLimitResponse (with status=DENIED)                        │
    │  OUTPUT: JSONResponse with 429 status code                             │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    HTTP/1.1 429 Too Many Requests                                      │
    │    X-RateLimit-Limit: 100                                              │
    │    X-RateLimit-Remaining: 0                                            │
    │    Retry-After: 12                                                     │
    │    {"error": "Rate limit exceeded", ...}                               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
