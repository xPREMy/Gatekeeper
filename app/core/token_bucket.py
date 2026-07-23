import time
from typing import Tuple
import redis.asyncio as aioredis
from .redis_client import redis_client

# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Write the Lua script
# ─────────────────────────────────────────────────────────────────────────────

TOKEN_BUCKET_LUA_SCRIPT = """
local key = KEYS[1]

local max_tokens = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local current_timestamp = tonumber(ARGV[3])
local requested_tokens = tonumber(ARGV[4])

if refill_rate <=0 then 
    return redis.error_reply("refill_rate must be positive")
end

local tokens = tonumber(redis.call("HGET",key,"tokens"))
local last_refill = tonumber(redis.call("HGET",key,"last_refill"))

if tokens == nil or last_refill == nil then 
    tokens = max_tokens
    last_refill = current_timestamp
end

local elapsed = current_timestamp - last_refill
local new_tokens = tokens + elapsed*refill_rate
new_tokens = math.min(new_tokens,max_tokens)
last_refill = current_timestamp

local allowed = 0

if new_tokens >=requested_tokens then
    new_tokens = new_tokens - requested_tokens
    allowed =1
end

redis.call("HSET",key,"tokens",new_tokens,"last_refill",last_refill)

local ttl = 10 + math.ceil((max_tokens-new_tokens)/refill_rate)
redis.call("EXPIRE",key,ttl)
return {allowed,new_tokens}
"""


class TokenBucket:
    """
    Distributed Token Bucket rate limiter backed by Redis + Lua.
    """

    def __init__(self, redis_client: aioredis.Redis):
        self._redis_client = redis_client
        self._script_sha =None

    async def _load_script(self) -> str:
        if self._script_sha is not None :
            return self._script_sha
        self._script_sha = await self._redis_client.script_load(TOKEN_BUCKET_LUA_SCRIPT)
        return self._script_sha

    async def consume(
        self,
        client_id: str,
        max_tokens: int,
        window_seconds: int,
        tokens_to_consume: int = 1,
    ) -> Tuple[bool, float]:
        
        refill_rate = max_tokens/window_seconds
        current_time = time.time()
        redis_key = f"RateLimit:{client_id}"
        sha= await self._load_script()
        result = await self._redis_client.evalsha(sha,1,redis_key,max_tokens,refill_rate,current_time,tokens_to_consume)

        allowed = bool(int(result[0]))
        remaining_tokens = float(result[1])
        return (allowed,remaining_tokens)

