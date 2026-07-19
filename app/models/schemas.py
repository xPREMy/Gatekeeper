"""
===============================================================================
MODULE 2: Pydantic Schemas (schemas.py)
Difficulty: ★☆☆☆☆ (Easy)
Phase: 1
===============================================================================

PROBLEM STATEMENT:
    Define the request/response data shapes used throughout the API.
    These are Pydantic models that FastAPI uses for automatic validation,
    serialization, and OpenAPI docs.

CONCEPTS:
    - Pydantic BaseModel
    - Field validation
    - JSON-serializable response models
===============================================================================
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Define RateLimitStatus enum
# ─────────────────────────────────────────────────────────────────────────────
class RateLimitStatus(str, Enum):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create an enum with two values:                                 │
    │    - ALLOWED  = "allowed"                                              │
    │    - DENIED   = "denied"                                               │
    │                                                                        │
    │  USAGE: Used in RateLimitResponse to indicate if request passed.       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: Client rate-limit configuration model
# ─────────────────────────────────────────────────────────────────────────────
class ClientRateLimitConfig(BaseModel):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Define a model for per-client rate-limit configuration.         │
    │                                                                        │
    │  FIELDS:                                                               │
    │    client_id      : str   → The unique identifier for the client       │
    │    max_requests   : int   → Max requests allowed per window            │
    │                             (must be > 0, default 100)                 │
    │    window_seconds : int   → Time window in seconds                     │
    │                             (must be > 0, default 60)                  │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    config = ClientRateLimitConfig(client_id="service-a",               │
    │                                   max_requests=50,                     │
    │                                   window_seconds=30)                   │
    │    >>> config.client_id  →  "service-a"                                │
    │                                                                        │
    │  HINT: Use Field(..., gt=0) for positive-int validation.               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: Rate-limit check response model
# ─────────────────────────────────────────────────────────────────────────────
class RateLimitResponse(BaseModel):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Define the response returned after a rate-limit check.          │
    │                                                                        │
    │  FIELDS:                                                               │
    │    status          : RateLimitStatus → ALLOWED or DENIED               │
    │    client_id       : str             → Who was checked                 │
    │    remaining       : int             → Remaining requests in window    │
    │    limit           : int             → Max requests configured         │
    │    retry_after     : Optional[float] → Seconds until tokens refill     │
    │                                        (None if allowed)               │
    │                                                                        │
    │  EXAMPLE (allowed):                                                    │
    │    {"status": "allowed", "client_id": "svc-a",                         │
    │     "remaining": 47, "limit": 100, "retry_after": null}               │
    │                                                                        │
    │  EXAMPLE (denied):                                                     │
    │    {"status": "denied", "client_id": "svc-a",                          │
    │     "remaining": 0, "limit": 100, "retry_after": 12.5}                │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Health check response model
# ─────────────────────────────────────────────────────────────────────────────
class HealthResponse(BaseModel):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Define a simple health-check response.                          │
    │                                                                        │
    │  FIELDS:                                                               │
    │    status      : str  → "healthy" or "unhealthy"                       │
    │    redis_connected : bool → Whether Redis is reachable                 │
    │    version     : str  → App version from settings                      │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    {"status": "healthy", "redis_connected": true, "version": "1.0.0"}  │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5: Generic gateway response model
# ─────────────────────────────────────────────────────────────────────────────
class GatewayResponse(BaseModel):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: A generic wrapper for all gateway responses.                    │
    │                                                                        │
    │  FIELDS:                                                               │
    │    success     : bool             → Did the request succeed?           │
    │    message     : str              → Human-readable message             │
    │    data        : Optional[dict]   → Any payload (default None)         │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    {"success": true, "message": "OK", "data": {"key": "value"}}        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
