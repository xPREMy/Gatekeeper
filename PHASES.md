# 🏰 Gatekeeper — Build Phases Guide

> **Distributed Rate Limiter / API Gateway**
> Python · FastAPI · Redis · Docker

This guide breaks the project into **6 phases**, ordered by dependency.
Each phase builds on the previous one. Within each phase, modules are
listed like LeetCode problems with difficulty ratings.

---

## 📋 How to Use This Guide

1. **Work phase by phase** — don't skip ahead
2. **Open each file** — read the docstrings like a problem statement
3. **Write the code** where you see `pass  # YOUR CODE HERE`
4. **Test each module** before moving to the next
5. **Each function** has: Input → Output → Examples → Hints

---

## Architecture Overview

```
                    ┌──────────────────────────────────────────────┐
                    │              CLIENT REQUEST                  │
                    │    (with X-API-Key or IP identification)     │
                    └──────────────────┬───────────────────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────────────┐
                    │          RATE LIMIT MIDDLEWARE               │
                    │    (Module 8: rate_limit_middleware.py)      │
                    │                                              │
                    │  1. Extract client ID (Module 6)             │
                    │  2. Check rate limit (Module 5)              │
                    │  3. Allow → add headers → forward            │
                    │     Deny  → return 429                       │
                    └──────────┬───────────────┬───────────────────┘
                               │               │
                          ALLOWED           DENIED
                               │               │
                               ▼               ▼
                    ┌──────────────────┐  ┌──────────────────────┐
                    │  ROUTE HANDLERS  │  │  429 Too Many        │
                    │  (Modules 9-11)  │  │  Requests Response   │
                    │  /health         │  │  (Module 7)          │
                    │  /admin/*        │  └──────────────────────┘
                    │  /api/*          │
                    └──────────────────┘
                               │
                    ┌──────────┴───────────────────────────────────┐
                    │          RATE LIMITER SERVICE                │
                    │    (Module 5: rate_limiter.py)               │
                    │                                              │
                    │  - Per-client config management (CRUD)       │
                    │  - Delegates to Token Bucket                 │
                    └──────────────────┬───────────────────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────────────┐
                    │         TOKEN BUCKET ALGORITHM               │
                    │    (Module 4: token_bucket.py)    ★ CORE ★  │
                    │                                              │
                    │  - Lua script for atomic operations          │
                    │  - Refill tokens over time                   │
                    │  - Consume tokens per request                │
                    └──────────────────┬───────────────────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────────────┐
                    │               REDIS                          │
                    │    (Module 3: redis_client.py)               │
                    │                                              │
                    │  - Token bucket state (hash per client)      │
                    │  - Client configs (JSON per client)          │
                    │  - Shared across all app instances           │
                    └──────────────────────────────────────────────┘
```

---

## ⏱ Estimated Total Time: 8–12 hours

---

## Phase 1 — Foundation (Config & Data Models)
**⏱ ~45 min** | No dependencies — start here

These are the building blocks everything else imports. Pure Python, no
Redis needed yet.

| # | Module | File | Difficulty | Tasks |
|---|--------|------|------------|-------|
| 1 | Config Loader | `app/config.py` | ★☆☆☆☆ | Define Settings class, `get_settings()` |
| 2 | Pydantic Schemas | `app/models/schemas.py` | ★☆☆☆☆ | 5 models: Enum, ClientConfig, RateLimitResponse, HealthResponse, GatewayResponse |

### ✅ Phase 1 Checklist
- [ ] `Settings` class loads from env vars with defaults
- [ ] `get_settings()` returns a cached singleton
- [ ] All 5 schema models are defined with proper fields
- [ ] You can instantiate each model in a Python REPL
- [ ] Copy `.env.example` → `.env`

### 🧪 Quick Verify
```python
# In a Python REPL
from app.config import get_settings
s = get_settings()
print(s.redis_host)  # → "localhost"

from app.models.schemas import ClientRateLimitConfig
c = ClientRateLimitConfig(client_id="test", max_requests=50, window_seconds=30)
print(c.model_dump_json())
```

---

## Phase 2 — The Engine (Redis + Token Bucket)
**⏱ ~2-3 hours** | Depends on: Phase 1

This is the **hardest and most important phase**. The token bucket
algorithm with the Lua script is the core intellectual challenge.

| # | Module | File | Difficulty | Tasks |
|---|--------|------|------------|-------|
| 3 | Redis Client | `app/core/redis_client.py` | ★★☆☆☆ | `connect()`, `disconnect()`, `get_client()`, `is_healthy()` |
| 4 | Token Bucket | `app/core/token_bucket.py` | ★★★★☆ | Lua script + `_load_script()`, `consume()` |

### 🔑 Key Challenge: The Lua Script
The Lua script in `token_bucket.py` is the heart of the project.
It must run **atomically** in Redis to prevent race conditions when
multiple gateway instances check the same client's rate limit
simultaneously.

### ✅ Phase 2 Checklist
- [ ] `RedisClient` can connect to a local Redis (`docker run -p 6379:6379 redis:7-alpine`)
- [ ] `is_healthy()` returns True when connected, False when not
- [ ] Lua script handles first-time requests (bucket initialization)
- [ ] Lua script correctly refills tokens based on elapsed time
- [ ] Lua script caps tokens at max_tokens
- [ ] `consume()` returns `(True, remaining)` when tokens available
- [ ] `consume()` returns `(False, 0)` when bucket is empty
- [ ] All `test_token_bucket.py` tests pass

### 🧪 Quick Verify
```python
# Start Redis first: docker run -p 6379:6379 redis:7-alpine
# Then run: pytest tests/test_token_bucket.py -v
```

---

## Phase 3 — The Service Layer
**⏱ ~1.5-2 hours** | Depends on: Phase 2

Connect the token bucket to the outside world. Add per-client config
management and the client identification utility.

| # | Module | File | Difficulty | Tasks |
|---|--------|------|------------|-------|
| 5 | Rate Limiter Service | `app/core/rate_limiter.py` | ★★★☆☆ | `set/get/delete/list_client_config()`, `check_rate_limit()` |
| 6 | Client Identifier | `app/utils/client_identifier.py` | ★★☆☆☆ | `extract_api_key()`, `extract_client_ip()`, `get_client_identifier()` |

### ✅ Phase 3 Checklist
- [ ] Can store a client config in Redis and retrieve it
- [ ] Unknown clients get default config from Settings
- [ ] `check_rate_limit()` returns ALLOWED/DENIED correctly
- [ ] API key extraction from `X-API-Key` and `Authorization: Bearer` headers
- [ ] IP extraction from `X-Forwarded-For`, `X-Real-IP`, and direct connection
- [ ] All `test_rate_limiter.py` tests pass

---

## Phase 4 — The API Layer (Routes + Middleware)
**⏱ ~2-3 hours** | Depends on: Phase 3

Build the HTTP interface. The middleware ties everything together.

| # | Module | File | Difficulty | Tasks |
|---|--------|------|------------|-------|
| 7 | Response Builder | `app/utils/response_builder.py` | ★☆☆☆☆ | `build_rate_limit_headers()`, `build_rate_limited_response()` |
| 8 | Rate Limit Middleware | `app/middleware/rate_limit_middleware.py` | ★★★☆☆ | `dispatch()` — the main interception logic |
| 9 | Health Route | `app/routes/health.py` | ★☆☆☆☆ | `GET /health` |
| 10 | Admin Routes | `app/routes/admin.py` | ★★☆☆☆ | CRUD: `POST/GET/DELETE /admin/clients` |
| 11 | Gateway Routes | `app/routes/gateway.py` | ★★☆☆☆ | `GET/POST /api/resource`, `GET /api/status` |

### ✅ Phase 4 Checklist
- [ ] Response builder creates correct rate-limit headers
- [ ] 429 response includes `Retry-After` header
- [ ] Middleware passes through requests to excluded paths (`/health`, `/docs`)
- [ ] Middleware blocks requests when rate limit is exceeded
- [ ] Middleware adds `X-RateLimit-*` headers to allowed responses
- [ ] Health endpoint reports Redis connection status
- [ ] Admin CRUD endpoints work (create, read, list, delete configs)
- [ ] Gateway endpoints return mock data

---

## Phase 5 — Wiring & Integration
**⏱ ~1-2 hours** | Depends on: Phase 4

Wire everything together in `main.py` and run the full app.

| # | Module | File | Difficulty | Tasks |
|---|--------|------|------------|-------|
| 12 | Main App | `app/main.py` | ★★★☆☆ | `lifespan()`, `create_app()`, uvicorn runner |

### ✅ Phase 5 Checklist
- [ ] App starts with `python -m app.main` (Redis must be running)
- [ ] `GET /health` returns healthy status
- [ ] `GET /docs` shows Swagger UI with all endpoints
- [ ] Rate limiting works end-to-end (test with curl or Postman):
  ```bash
  # Set a low limit
  curl -X POST http://localhost:8000/admin/clients \
    -H "Content-Type: application/json" \
    -d '{"client_id": "test", "max_requests": 5, "window_seconds": 60}'

  # Hit the endpoint 6 times
  for i in $(seq 1 6); do
    curl -s -o /dev/null -w "%{http_code}" \
      -H "X-API-Key: test" \
      http://localhost:8000/api/resource
    echo ""
  done
  # Expected: 200 200 200 200 200 429
  ```
- [ ] All `test_integration.py` tests pass

---

## Phase 6 — Containerization (Docker)
**⏱ ~1-2 hours** | Depends on: Phase 5

Containerize and prove it works across multiple instances.

| # | File | Difficulty | Tasks |
|---|------|------------|-------|
| 13 | `Dockerfile` | ★★☆☆☆ | Multi-stage build, non-root user, healthcheck |
| 14 | `docker-compose.yml` | ★★☆☆☆ | Redis + 2x Gatekeeper instances |

### ✅ Phase 6 Checklist
- [ ] `docker build -t gatekeeper .` succeeds
- [ ] `docker-compose up --build` starts Redis + Gatekeeper
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Rate limiting works through Docker
- [ ] **MULTI-INSTANCE TEST**: Both port 8000 and 8001 share rate limits:
  ```bash
  # Set limit to 3 for "test-key"
  curl -X POST http://localhost:8000/admin/clients \
    -H "Content-Type: application/json" \
    -d '{"client_id": "test-key", "max_requests": 3, "window_seconds": 60}'

  # Hit instance 1 twice
  curl -H "X-API-Key: test-key" http://localhost:8000/api/resource  # 200
  curl -H "X-API-Key: test-key" http://localhost:8000/api/resource  # 200

  # Hit instance 2 once
  curl -H "X-API-Key: test-key" http://localhost:8001/api/resource  # 200

  # Hit either instance — should be denied!
  curl -H "X-API-Key: test-key" http://localhost:8000/api/resource  # 429
  curl -H "X-API-Key: test-key" http://localhost:8001/api/resource  # 429
  ```
- [ ] `docker-compose down` cleans up gracefully

---

## 🎯 Final Project Structure

```
gatekeeper/
├── .env.example              # Phase 1 — env var template
├── .gitignore
├── .dockerignore
├── requirements.txt          # Phase 1 — dependencies
├── Dockerfile                # Phase 6 — container build
├── docker-compose.yml        # Phase 6 — multi-service orchestration
│
├── app/
│   ├── __init__.py
│   ├── config.py             # Module 1  ★☆☆☆☆  Phase 1
│   ├── main.py               # Module 12 ★★★☆☆  Phase 5
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Module 2  ★☆☆☆☆  Phase 1
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── redis_client.py   # Module 3  ★★☆☆☆  Phase 2
│   │   ├── token_bucket.py   # Module 4  ★★★★☆  Phase 2  ← BOSS LEVEL
│   │   └── rate_limiter.py   # Module 5  ★★★☆☆  Phase 3
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── rate_limit_middleware.py  # Module 8  ★★★☆☆  Phase 4
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py         # Module 9  ★☆☆☆☆  Phase 4
│   │   ├── admin.py          # Module 10 ★★☆☆☆  Phase 4
│   │   └── gateway.py        # Module 11 ★★☆☆☆  Phase 4
│   │
│   └── utils/
│       ├── __init__.py
│       ├── client_identifier.py   # Module 6  ★★☆☆☆  Phase 3
│       └── response_builder.py    # Module 7  ★☆☆☆☆  Phase 4
│
└── tests/
    ├── __init__.py
    ├── test_token_bucket.py   # Phase 2 tests
    ├── test_rate_limiter.py   # Phase 3 tests
    └── test_integration.py    # Phase 5 tests
```

---

## 🚀 Prerequisites Before You Start

1. **Python 3.12+** installed
2. **Docker** installed (for Redis and containerization)
3. **Redis** running locally:
   ```bash
   docker run -d -p 6379:6379 --name gatekeeper-redis redis:7-alpine
   ```
4. **Virtual environment**:
   ```bash
   cd gatekeeper
   python -m venv .venv
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

---

## 💡 Tips

- **Read each file top-to-bottom** — the problem statement, concepts, and
  hints are all there
- **Start with the easiest modules** (★☆☆☆☆) to build confidence
- **Module 4 (Token Bucket)** is the boss fight — take your time with
  the Lua script. Test it in `redis-cli` first if needed
- **Use `pytest -v`** after each phase to catch bugs early
- **The Swagger UI at `/docs`** is your best friend for testing routes

---

*Built with ❤️ for learning distributed systems, one function at a time.*
