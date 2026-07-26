from fastapi import APIRouter, HTTPException , Depends , status
from typing import List
from app.models.schemas import ClientRateLimitConfig, GatewayResponse
from app.core.rate_limiter import RateLimiterService
from app.utils.dependancies import get_rate_limiter

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/clients", response_model=GatewayResponse , status_code=status.HTTP_200_OK)
async def create_client_config(config: ClientRateLimitConfig, rate_limiter_service : RateLimiterService = Depends(get_rate_limiter)):
    try:
        await rate_limiter_service.set_client_config(config=config)
        return GatewayResponse(
            success=True,
            message=f"Config set for client '{config.client_id}'",
            data=config.model_dump()
        )
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/clients", response_model=List[ClientRateLimitConfig],status_code=status.HTTP_200_OK)
async def list_client_configs(rate_limiter_service : RateLimiterService = Depends(get_rate_limiter)):
    try:
        config_list = await rate_limiter_service.list_client_configs()
        return config_list
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
@router.get("/clients/{client_id}", response_model=ClientRateLimitConfig , status_code=status.HTTP_200_OK)
async def get_client_config(client_id: str,rate_limiter_service : RateLimiterService = Depends(get_rate_limiter)):
    try:
        config = await rate_limiter_service.get_client_config(client_id=client_id)
        return config
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        


@router.delete("/clients/{client_id}", response_model=GatewayResponse , status_code=status.HTTP_200_OK)
async def delete_client_config(client_id: str,rate_limiter_service : RateLimiterService = Depends(get_rate_limiter)):
    deleted = rate_limiter_service.delete_client_config(client_id=client_id)
    if deleted is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="client-id is not configured")
    return GatewayResponse(
        success=True,
        message=f"Config deleted successfully for client-id : {client_id}"
    )