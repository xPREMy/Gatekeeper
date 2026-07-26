from fastapi import APIRouter, Request
from app.models.schemas import GatewayResponse

router = APIRouter(tags=["Gateway"])

@router.get("/api/resource", response_model=GatewayResponse)
async def get_resource(request: Request):
    return GatewayResponse(
        success=True,
        message="Resource fetched successfully",
        data={
            "resource_id": "sample-123",                             
            "name": "Sample Resource",                               
            "description": "This request passed rate limiting" 
        }
    )

@router.post("/api/resource", response_model=GatewayResponse)
async def create_resource(request: Request):
    return GatewayResponse(
            success=True,
            message="Resource created successfully",
            data={
                "resource_id": "sample-123",                             
                "name": "Sample Resource",                               
                "description": "This request passed rate limiting" 
            }
        )

@router.get("/api/status", response_model=GatewayResponse)
async def get_status():
    return GatewayResponse(
                success=True,
                message="Gateway is operational",
                data={
                    "resource_id": "sample-123",                             
                    "name": "Sample Resource",                               
                    "description": "This request passed rate limiting" 
                }
            )
