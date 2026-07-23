from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class RateLimitStatus(str, Enum):

    ALLOWED  = "allowed" 
    DENIED   = "denied"  

class ClientRateLimitConfig(BaseModel):

    client_id :str
    max_requests : int = Field(gt=0)
    window_seconds : int = Field(gt=0)

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
    status : RateLimitStatus
    Client_id : str
    remaining : int
    limit : int
    retry_after : Optional[float] # None if allowed

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
    status : str 
    redis_connected : bool 
    version : str 

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
    success : bool
    message : str
    data : Optional[dict]
