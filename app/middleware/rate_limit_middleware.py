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
        super().__init__(app)
        self._rate_limiter = rate_limiter  # service object
        self._excluded_paths = excluded_paths

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self._excluded_paths:
            return await call_next(request)

        client_id = get_client_identifier(request=request)
        result = await self._rate_limiter.check_rate_limit(client_id=client_id)

        if result.status == RateLimitStatus.DENIED :
            return build_rate_limited_response(result)

        response = await call_next(result)
        header = build_rate_limit_headers(result)

        for key , value in header.items():
            response.headers[key] = value  

        return response
