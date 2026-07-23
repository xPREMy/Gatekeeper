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

from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME : str = "Gatekeeper"
    APP_VERSION : str ="0.1"
    DEBUG : bool =  False

    REDIS_HOST : str = "localhost"
    REDIS_PORT : int = 6379
    REDIS_DB : int = 0
    REDIS_PASSWORD : Optional[str]
    REDIS_URL : Optional[str]

    DEFAULT_RATE_LIMIT : int =100
    DEFAULT_WINDOW_SECONDS : int = 60
    Tokens_consume_per_request : int = 1
    SERVER_HOST : str
    SERVER_PORT : str
    
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
