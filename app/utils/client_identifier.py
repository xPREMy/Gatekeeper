"""
===============================================================================
MODULE 6: Client Identifier Utility (client_identifier.py)
Difficulty: ★★☆☆☆ (Easy-Medium)
Phase: 3
===============================================================================

PROBLEM STATEMENT:
    Extract a unique client identifier from an incoming HTTP request.
    The gateway needs to know WHO is making the request to apply the
    correct rate limit. Support multiple identification strategies.

CONCEPTS:
    - HTTP headers (X-API-Key, Authorization)
    - IP-based fallback
    - Strategy pattern
===============================================================================
"""

from fastapi import Request
from typing import Optional


def extract_api_key(request: Request) -> Optional[str]:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Extract API key from the request headers.                      │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Check header "X-API-Key" → return its value if present           │
    │    2. Check header "Authorization":                                    │
    │       - If it starts with "Bearer " → return the part after "Bearer " │
    │    3. If neither found → return None                                   │
    │                                                                        │
    │  INPUT:  FastAPI Request object                                        │
    │  OUTPUT: Optional[str] — the API key, or None                          │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    # Request with header: X-API-Key: abc123                            │
    │    >>> extract_api_key(request)  →  "abc123"                           │
    │                                                                        │
    │    # Request with header: Authorization: Bearer xyz789                 │
    │    >>> extract_api_key(request)  →  "xyz789"                           │
    │                                                                        │
    │    # Request with no key headers                                       │
    │    >>> extract_api_key(request)  →  None                               │
    │                                                                        │
    │  HINT: request.headers.get("X-API-Key") returns None if missing        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


def extract_client_ip(request: Request) -> str:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Extract the client's IP address from the request.              │
    │                                                                        │
    │  STEPS:                                                                │
    │    1. Check header "X-Forwarded-For":                                  │
    │       - If present → return the FIRST IP (split by ",")[0].strip()     │
    │       - (Proxies append IPs; the first one is the original client)     │
    │    2. Check header "X-Real-IP" → return if present                    │
    │    3. Fallback: return request.client.host                             │
    │    4. If all fail → return "unknown"                                   │
    │                                                                        │
    │  INPUT:  FastAPI Request object                                        │
    │  OUTPUT: str — IP address string                                       │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    # Behind a proxy: X-Forwarded-For: 203.0.113.50, 70.41.3.18        │
    │    >>> extract_client_ip(request)  →  "203.0.113.50"                   │
    │                                                                        │
    │    # Direct connection                                                 │
    │    >>> extract_client_ip(request)  →  "127.0.0.1"                      │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE


def get_client_identifier(request: Request) -> str:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  TASK: Determine the unique client identifier for rate limiting.      │
    │                                                                        │
    │  STRATEGY:                                                             │
    │    1. Try extract_api_key(request) first                               │
    │    2. If no API key → fall back to extract_client_ip(request)          │
    │    3. Return whatever was found                                        │
    │                                                                        │
    │  INPUT:  FastAPI Request object                                        │
    │  OUTPUT: str — a unique client identifier                              │
    │                                                                        │
    │  EXAMPLE:                                                              │
    │    # With X-API-Key header                                             │
    │    >>> get_client_identifier(request)  →  "abc123"                     │
    │                                                                        │
    │    # Without any key header                                            │
    │    >>> get_client_identifier(request)  →  "192.168.1.100"              │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    pass  # YOUR CODE HERE
