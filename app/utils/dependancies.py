from fastapi import Request
from app.core.rate_limiter import RateLimiterService

def get_rate_limiter(request: Request) -> RateLimiterService:
    return request.app.state.rate_limiter