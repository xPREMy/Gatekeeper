from fastapi import Request
from typing import Optional


def extract_api_key(request: Request) -> Optional[str]:
    api_key = request.headers.get("X-API-key")
    if api_key is not None:
        return api_key
    auth  = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth[7:]
    return None

def extract_client_ip(request: Request) -> str:
    ip = request.headers.get("X-Forwarded-For")
    if ip is not None:
        ip= ip.split(",")[0].strip()
        return ip

    ip = request.headers.get("X-Real-IP")
    if ip is not None:
        return ip

    ip = request.client.host
    if ip is not None:
        return ip

    return "unknown"


def get_client_identifier(request: Request) -> str:
    api_key = extract_api_key(request=request)
    if api_key is not None:
        return api_key
    ip = extract_client_ip(request=request)
    return ip
