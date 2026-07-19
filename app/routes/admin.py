"""
===============================================================================
MODULE 10: Admin Routes (admin.py)
Difficulty: ★★☆☆☆ (Easy-Medium)
Phase: 4
===============================================================================

PROBLEM STATEMENT:
    Create admin API endpoints for managing per-client rate-limit
    configurations at runtime. These let ops teams configure, inspect,
    and remove rate limits without redeploying.

CONCEPTS:
    - FastAPI APIRouter with prefix
    - CRUD operations via REST
    - Dependency injection
===============================================================================
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import ClientRateLimitConfig, GatewayResponse
from app.core.rate_limiter import RateLimiterService


router = APIRouter(prefix="/admin", tags=["Admin"])

# ─────────────────────────────────────────────────────────────────────────────
# NOTE: You'll need to figure out how to get the RateLimiterService instance
# into these route handlers. Options:
#   A) Use FastAPI's Depends() with a dependency function
#   B) Store it on app.state during startup and access via request.app.state
#   C) Use a module-level variable set during app initialization
#
# Pick ONE approach and be consistent. Option B is recommended for this project.
# ─────────────────────────────────────────────────────────────────────────────


@router.post("/clients", response_model=GatewayResponse)
async def create_client_config(config: ClientRateLimitConfig):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Create or update a client's rate-limit configuration.          │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get the rate_limiter service instance                            │
    │    2. await rate_limiter.set_client_config(config)                     │
    │    3. Return GatewayResponse(                                          │
    │           success=True,                                                │
    │           message=f"Config set for client '{config.client_id}'",       │
    │           data=config.model_dump())                                    │
    │                                                                        │
    │  INPUT:  ClientRateLimitConfig (from request body JSON)                │
    │  OUTPUT: GatewayResponse                                               │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    POST /admin/clients                                                 │
    │    Body: {"client_id": "svc-a", "max_requests": 50, "window_seconds": 30}
    │    → 200 {"success": true, "message": "Config set for client 'svc-a'",│
    │           "data": {"client_id": "svc-a", ...}}                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@router.get("/clients", response_model=List[ClientRateLimitConfig])
async def list_client_configs():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: List all configured client rate limits.                         │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get the rate_limiter service instance                            │
    │    2. configs = await rate_limiter.list_client_configs()               │
    │    3. Return configs (FastAPI auto-serializes the list)                │
    │                                                                        │
    │  INPUT:  None                                                          │
    │  OUTPUT: List[ClientRateLimitConfig]                                   │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    GET /admin/clients                                                  │
    │    → 200 [{"client_id": "svc-a", "max_requests": 50, ...}, ...]       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@router.get("/clients/{client_id}", response_model=ClientRateLimitConfig)
async def get_client_config(client_id: str):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Get a specific client's rate-limit configuration.              │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get the rate_limiter service instance                            │
    │    2. config = await rate_limiter.get_client_config(client_id)         │
    │    3. Return config                                                    │
    │                                                                        │
    │  INPUT:  client_id (path parameter)                                    │
    │  OUTPUT: ClientRateLimitConfig                                         │
    │                                                                        │
    │  NOTE: If no custom config exists, this returns the default config.    │
    │        That's fine — the caller sees what limits actually apply.        │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    GET /admin/clients/svc-a                                            │
    │    → 200 {"client_id": "svc-a", "max_requests": 50, ...}              │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@router.delete("/clients/{client_id}", response_model=GatewayResponse)
async def delete_client_config(client_id: str):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Delete a client's custom config (reverts to defaults).         │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Get the rate_limiter service instance                            │
    │    2. deleted = await rate_limiter.delete_client_config(client_id)     │
    │    3. If not deleted → raise HTTPException(404, detail="...")          │
    │    4. If deleted → Return GatewayResponse(success=True, ...)          │
    │                                                                        │
    │  INPUT:  client_id (path parameter)                                    │
    │  OUTPUT: GatewayResponse or 404 error                                  │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    DELETE /admin/clients/svc-a                                          │
    │    → 200 {"success": true, "message": "Config deleted for 'svc-a'"}   │
    │                                                                        │
    │    DELETE /admin/clients/nonexistent                                    │
    │    → 404 {"detail": "No config found for client 'nonexistent'"}       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
