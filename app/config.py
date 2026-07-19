"""
===============================================================================
MODULE 1: Configuration Loader (config.py)
Difficulty: ★☆☆☆☆ (Easy)
Phase: 1
===============================================================================

PROBLEM STATEMENT:
    Build a configuration manager that loads settings from environment variables
    with sensible defaults. This is the backbone of the app — every other module
    reads from here.

CONCEPTS:
    - Pydantic BaseSettings for env-var parsing
    - .env file support
    - Centralized, typed configuration

REFERENCE:
    https://docs.pydantic.dev/latest/concepts/pydantic_settings/
===============================================================================
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Define all configuration fields with types and defaults.        │
    │                                                                        │
    │  FIELDS TO ADD:                                                        │
    │  ─────────────────────────────────────────────────────────────────────  │
    │  app_name          : str       → default "Gatekeeper"                  │
    │  app_version       : str       → default "1.0.0"                       │
    │  debug             : bool      → default False                         │
    │                                                                        │
    │  redis_host        : str       → default "localhost"                   │
    │  redis_port        : int       → default 6379                          │
    │  redis_db          : int       → default 0                             │
    │  redis_password    : Optional[str] → default None                      │
    │                                                                        │
    │  default_rate_limit : int      → default 100   (requests per window)   │
    │  default_window_seconds : int  → default 60    (window size)           │
    │                                                                        │
    │  server_host       : str       → default "0.0.0.0"                     │
    │  server_port       : int       → default 8000                          │
    │                                                                        │
    │  ALSO: Configure the inner `model_config` to read from a `.env` file.  │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    settings = Settings()                                               │
    │    >>> settings.redis_host  →  "localhost"                              │
    │    >>> settings.default_rate_limit  →  100                              │
    │                                                                        │
    │    # With env var REDIS_HOST=redis-server                              │
    │    settings = Settings()                                               │
    │    >>> settings.redis_host  →  "redis-server"                          │
    │                                                                        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


def get_settings() -> Settings:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Return a cached singleton instance of Settings.                 │
    │                                                                        │
    │  WHY: Creating Settings() every request is wasteful. Use               │
    │       @lru_cache or a module-level variable so it's created once.      │
    │                                                                        │
    │  INPUT:  None                                                          │
    │  OUTPUT: Settings instance (always the same object)                    │
    │                                                                        │
    │  HINT: from functools import lru_cache — decorate this function.       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
