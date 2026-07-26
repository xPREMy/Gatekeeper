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

    status : RateLimitStatus
    client_id : str
    remaining : int
    limit : int
    retry_after : Optional[float] # None if allowed

class HealthResponse(BaseModel):
    status : str 
    redis_connected : bool 
    version : str 

class GatewayResponse(BaseModel):
    success : bool
    message : str
    data : Optional[dict]
