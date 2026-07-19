"""
===============================================================================
MODULE 11: Gateway Routes (gateway.py)
Difficulty: ★★☆☆☆ (Easy-Medium)
Phase: 4
===============================================================================

PROBLEM STATEMENT:
    Create the main gateway endpoints that simulate a protected API.
    These are the endpoints that clients actually call, and they
    demonstrate the rate limiting in action.

    In a real API gateway, these would proxy to backend services.
    For this project, they return mock responses.

CONCEPTS:
    - FastAPI route handlers
    - Demonstrating the rate-limit middleware in action
    - Mock API responses
===============================================================================
"""

from fastapi import APIRouter, Request
from app.models.schemas import GatewayResponse

router = APIRouter(tags=["Gateway"])


@router.get("/api/resource", response_model=GatewayResponse)
async def get_resource(request: Request):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: A sample protected GET endpoint.                               │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Return GatewayResponse(                                          │
    │           success=True,                                                │
    │           message="Resource fetched successfully",                     │
    │           data={                                                       │
    │               "resource_id": "sample-123",                             │
    │               "name": "Sample Resource",                               │
    │               "description": "This request passed rate limiting"       │
    │           })                                                           │
    │                                                                        │
    │  NOTE: The rate limiting happens in the MIDDLEWARE before this         │
    │        handler is called. If you're here, the request was allowed.     │
    │                                                                        │
    │  INPUT:  Request (available but not required for the response)          │
    │  OUTPUT: GatewayResponse                                               │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    GET /api/resource                                                   │
    │    Headers: X-API-Key: my-key                                          │
    │    → 200 {"success": true, "message": "Resource fetched...", ...}      │
    │    → Headers: X-RateLimit-Limit: 100, X-RateLimit-Remaining: 99       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@router.post("/api/resource", response_model=GatewayResponse)
async def create_resource(request: Request):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: A sample protected POST endpoint.                              │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Return GatewayResponse(                                          │
    │           success=True,                                                │
    │           message="Resource created successfully",                     │
    │           data={"resource_id": "new-456", "status": "created"})       │
    │                                                                        │
    │  INPUT:  Request                                                       │
    │  OUTPUT: GatewayResponse                                               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


@router.get("/api/status", response_model=GatewayResponse)
async def get_status():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: A simple status endpoint (also rate-limited).                   │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Return GatewayResponse(                                          │
    │           success=True,                                                │
    │           message="Gateway is operational",                            │
    │           data={"gateway": "Gatekeeper", "status": "running"})        │
    │                                                                        │
    │  INPUT:  None                                                          │
    │  OUTPUT: GatewayResponse                                               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
