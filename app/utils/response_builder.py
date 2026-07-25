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
from fastapi import status
from app.models.schemas import RateLimitResponse, RateLimitStatus


def build_rate_limit_headers(rate_limit_result: RateLimitResponse) -> dict:
    header : dict = {
        "X-RateLimit-Limit" : str(rate_limit_result.limit),
        "X-RateLimit-Remaining" : str(rate_limit_result.remaining)
    }
    if rate_limit_result.retry_after is not None :
        header["Retry-After"] = str(int(rate_limit_result.retry_after))
        header["X-RateLimit-Reset"] = str(int(rate_limit_result.retry_after))

    return header


def build_rate_limited_response(rate_limit_result: RateLimitResponse) -> JSONResponse:
    headers = build_rate_limit_headers(rate_limit_result=rate_limit_result)
    return JSONResponse(
        status_code= status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",                         
            "client_id": rate_limit_result.client_id,                    
            "retry_after": rate_limit_result.retry_after
        },
        headers= headers
    )
