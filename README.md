# 🏰 Gatekeeper

**Distributed Rate Limiter / API Gateway**

A high-performance API gateway that enforces configurable per-client rate limits using a Redis-backed token bucket algorithm. Designed for correctness under concurrent, multi-instance load.

## Tech Stack

- **Python 3.12+** — Core language
- **FastAPI** — Async web framework
- **Redis** — Distributed state store
- **Docker** — Containerization & orchestration

## Features

- 🪣 **Token Bucket Algorithm** — Smooth, burst-friendly rate limiting
- 🔒 **Atomic Operations** — Redis Lua scripts prevent race conditions
- 🌐 **Distributed** — Multiple instances share rate-limit state via Redis
- ⚙️ **Per-Client Config** — Runtime-configurable limits per API key
- 🐳 **Dockerized** — One command to run the full stack
- 📊 **Standard Headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`

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

## Quick Start

```bash
# 1. Clone and enter
cd gatekeeper

# 2. Start Redis
docker run -d -p 6379:6379 --name gatekeeper-redis redis:7-alpine

# 3. Install deps
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# 4. Copy env
copy .env.example .env

# 5. Run
python -m app.main
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/admin/clients` | Set client rate-limit config |
| `GET` | `/admin/clients` | List all client configs |
| `GET` | `/admin/clients/{id}` | Get specific client config |
| `DELETE` | `/admin/clients/{id}` | Delete client config |
| `GET` | `/api/resource` | Sample protected endpoint |
| `POST` | `/api/resource` | Sample protected endpoint |
| `GET` | `/api/status` | Gateway status |

## License

MIT
