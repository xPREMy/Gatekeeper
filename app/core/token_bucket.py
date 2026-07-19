"""
===============================================================================
MODULE 4: Token Bucket Algorithm (token_bucket.py)
Difficulty: ★★★★☆ (Hard) — THE CORE ALGORITHM
Phase: 2
===============================================================================

PROBLEM STATEMENT:
    Implement the Token Bucket rate limiting algorithm backed by Redis.

    The token bucket works like this:
    - Each client has a "bucket" that holds tokens (stored in Redis).
    - The bucket has a max capacity (e.g., 100 tokens).
    - Tokens are added at a constant rate (e.g., 100 tokens per 60 seconds).
    - Each request consumes 1 token.
    - If the bucket is empty → request is DENIED.
    - If the bucket has tokens → request is ALLOWED, and 1 token is removed.

    Because multiple app instances share the same Redis, this must be
    ATOMIC — use a Redis Lua script to avoid race conditions.

CONCEPTS:
    - Token Bucket algorithm
    - Redis Lua scripting for atomicity
    - Distributed state via Redis keys
    - Time-based token replenishment

WHY LUA SCRIPT?
    Without Lua, you'd do: GET → compute → SET. Between GET and SET,
    another instance could also GET the old value → both think there are
    tokens → you over-serve. A Lua script runs atomically inside Redis.
===============================================================================
"""

import time
from typing import Tuple
import redis.asyncio as aioredis


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Write the Lua script
# ─────────────────────────────────────────────────────────────────────────────

TOKEN_BUCKET_LUA_SCRIPT = """
--[[
┌─────────────────────────────────────────────────────────────────────────────┐
│  TASK: Write a Lua script that runs atomically in Redis.                   │
│                                                                            │
│  KEYS[1] = Redis key for this client's bucket (e.g. "ratelimit:client-a")  │
│                                                                            │
│  ARGV[1] = max_tokens       (bucket capacity, e.g. 100)                    │
│  ARGV[2] = refill_rate      (tokens added per second, e.g. 1.667)          │
│  ARGV[3] = now              (current timestamp as float, e.g. 1721406000)  │
│  ARGV[4] = requested        (tokens to consume, usually 1)                 │
│                                                                            │
│  ALGORITHM:                                                                │
│    1. Read current state from the Redis hash at KEYS[1]:                   │
│       - "tokens"      → current token count (float)                        │
│       - "last_refill" → timestamp of last refill (float)                   │
│                                                                            │
│    2. If key doesn't exist (first request):                                │
│       - Set tokens = max_tokens                                            │
│       - Set last_refill = now                                              │
│                                                                            │
│    3. Calculate tokens to add since last refill:                            │
│       - elapsed = now - last_refill                                        │
│       - new_tokens = tokens + (elapsed * refill_rate)                      │
│       - Cap at max_tokens: new_tokens = min(new_tokens, max_tokens)        │
│       - Update last_refill = now                                           │
│                                                                            │
│    4. Check if enough tokens:                                              │
│       - If new_tokens >= requested:                                        │
│           → Subtract requested from new_tokens                             │
│           → Save state back to hash                                        │
│           → Return {1, new_tokens}    -- 1 = allowed                       │
│       - Else:                                                              │
│           → Save state back (with refilled tokens, but don't subtract)     │
│           → Return {0, new_tokens}    -- 0 = denied                        │
│                                                                            │
│    5. Set a TTL on the key so stale buckets auto-expire:                   │
│       - TTL = (max_tokens / refill_rate) + 10  seconds                     │
│                                                                            │
│  RETURN: Array of two numbers → {allowed (0 or 1), remaining_tokens}       │
│                                                                            │
│  HINT: Use redis.call("HGET", ...), redis.call("HSET", ...),              │
│        redis.call("EXPIRE", ...), tonumber(), math.min()                   │
└─────────────────────────────────────────────────────────────────────────────┘
--]]

-- YOUR LUA CODE HERE
return {0, 0}
"""


class TokenBucket:
    """
    Distributed Token Bucket rate limiter backed by Redis + Lua.
    """

    def __init__(self, redis_client: aioredis.Redis):
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Store the redis client and register the Lua script.         │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Store redis_client as self._redis                            │
        │    2. Set self._script_sha = None (will be set in _load_script)    │
        │                                                                    │
        │  NOTE: Script registration happens lazily in _load_script().       │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def _load_script(self) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Register the Lua script with Redis and cache the SHA.       │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. If self._script_sha is already set → return it               │
        │    2. Otherwise: sha = await self._redis.script_load(              │
        │                            TOKEN_BUCKET_LUA_SCRIPT)                │
        │    3. Cache: self._script_sha = sha                                │
        │    4. Return sha                                                   │
        │                                                                    │
        │  INPUT:  None                                                      │
        │  OUTPUT: str — the SHA1 hash of the registered script              │
        │                                                                    │
        │  WHY: script_load sends the script once; then evalsha runs it      │
        │       by hash, saving bandwidth on repeated calls.                 │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE

    async def consume(
        self,
        client_id: str,
        max_tokens: int,
        window_seconds: int,
        tokens_to_consume: int = 1,
    ) -> Tuple[bool, float]:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │  TASK: Attempt to consume token(s) from a client's bucket.         │
        │                                                                    │
        │  This is the main entry point. It runs the Lua script.             │
        │                                                                    │
        │  STEPS:                                                            │
        │    1. Compute refill_rate = max_tokens / window_seconds            │
        │    2. Build the Redis key: f"ratelimit:{client_id}"                │
        │    3. Get current time: now = time.time()                          │
        │    4. Load the script SHA: sha = await self._load_script()         │
        │    5. Execute: result = await self._redis.evalsha(                 │
        │           sha, 1,    ← number of KEYS                             │
        │           key,       ← KEYS[1]                                    │
        │           str(max_tokens), str(refill_rate),                       │
        │           str(now), str(tokens_to_consume)                         │
        │       )                                                            │
        │    6. Parse result:                                                │
        │       - allowed = bool(int(result[0]))                             │
        │       - remaining = float(result[1])                               │
        │    7. Return (allowed, remaining)                                  │
        │                                                                    │
        │  INPUT:                                                            │
        │    client_id        : str  → "service-a"                           │
        │    max_tokens        : int  → 100                                  │
        │    window_seconds    : int  → 60                                   │
        │    tokens_to_consume : int  → 1 (usually)                          │
        │                                                                    │
        │  OUTPUT: Tuple[bool, float]                                        │
        │    - (True, 99.0)  → Request allowed, 99 tokens left              │
        │    - (False, 0.0)  → Request denied, 0 tokens left                │
        │                                                                    │
        │  EXAMPLE:                                                          │
        │    bucket = TokenBucket(redis)                                     │
        │    allowed, remaining = await bucket.consume("svc-a", 100, 60)     │
        │    >>> (True, 99.0)                                                │
        │    # ... after 100 more calls ...                                  │
        │    >>> (False, 0.0)                                                │
        │                                                                    │
        │  EDGE CASES:                                                       │
        │    - First request ever for a client → bucket starts full          │
        │    - tokens_to_consume > max_tokens → always denied                │
        │    - Concurrent calls from multiple instances → Lua ensures safety │
        └─────────────────────────────────────────────────────────────────────┘
        """
        pass  # YOUR CODE HERE
