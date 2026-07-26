from contextlib import asynccontextmanager
from fastapi import FastAPI , HTTPException, status

from app.config import get_settings
from app.core.redis_client import redis_client
from app.core.token_bucket import TokenBucket
from app.core.rate_limiter import RateLimiterService
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.routes import health, admin, gateway
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    
    try:
        await redis_client.connect()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    token_bucket = TokenBucket(redis=redis_client.get_client())
    rate_limit_service = RateLimiterService(token_bucket)
    app.state.rate_limiter = rate_limit_service
    yield
    await redis_client.disconnect()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Gatekeeper API Gateway",
        description="Distributed Rate Limiter & API Gateway",
        version=get_settings().APP_VERSION,
        lifespan=lifespan
    )
    app.add_middleware(
        RateLimitMiddleware,
        excluded_paths=["/docs","/health","/admin","/openapi.json"]
    )

app = None  # YOUR CODE HERE — replace with create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )

