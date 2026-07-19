# ═══════════════════════════════════════════════════════════════════════════════
# Gatekeeper Dockerfile
# Phase: 6 — Containerization
# ═══════════════════════════════════════════════════════════════════════════════
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  TASK: Build a multi-stage Dockerfile for the Gatekeeper service.        │
# │                                                                            │
# │  REQUIREMENTS:                                                             │
# │    Base image: python:3.12-slim                                            │
# │    Working dir: /app                                                       │
# │    Must install requirements.txt first (for Docker layer caching)          │
# │    Copy app code AFTER installing deps                                     │
# │    Expose port 8000                                                        │
# │    Run with: uvicorn app.main:app --host 0.0.0.0 --port 8000             │
# │                                                                            │
# │  STEPS:                                                                    │
# │    1. FROM python:3.12-slim                                                │
# │    2. WORKDIR /app                                                         │
# │    3. COPY requirements.txt .                                              │
# │    4. RUN pip install --no-cache-dir -r requirements.txt                   │
# │    5. COPY . .                                                             │
# │    6. EXPOSE 8000                                                          │
# │    7. CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port","8000"]│
# │                                                                            │
# │  BONUS:                                                                    │
# │    - Add a HEALTHCHECK instruction that curls /health                      │
# │    - Use a non-root user for security                                      │
# │    - Add .dockerignore to skip __pycache__, .env, .git, tests             │
# └─────────────────────────────────────────────────────────────────────────────┘

# YOUR DOCKERFILE HERE
