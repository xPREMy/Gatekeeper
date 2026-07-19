from app.config import get_settings
s = get_settings()
print(s.REDIS_HOST)  

from app.models.schemas import ClientRateLimitConfig
c = ClientRateLimitConfig(client_id="test", max_requests=50, window_seconds=30)
print(c.model_dump_json())