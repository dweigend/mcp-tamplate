"""⚙️ Configuration Resource - Example implementation."""

from typing import Any, Dict

from src.config import (
    BATCH_SIZE,
    CACHE_SIZE,
    DEBUG_MODE,
    DEFAULT_TIMEOUT,
    ENABLE_LOGGING,
    MAX_RETRIES,
    SEARCH_DEFAULT_LIMIT,
    SEARCH_MAX_RESULTS,
    SERVER_NAME,
    VERSION,
)


def get_safe_configuration() -> Dict[str, Any]:
    """Get current server configuration (safe subset)."""
    return {
        "server": {
            "name": SERVER_NAME,
            "version": VERSION,
            "debug_mode": DEBUG_MODE
        },
        "limits": {
            "default_timeout": DEFAULT_TIMEOUT,
            "max_retries": MAX_RETRIES,
            "batch_size": BATCH_SIZE,
            "cache_size": CACHE_SIZE
        },
        "search": {
            "default_limit": SEARCH_DEFAULT_LIMIT,
            "max_results": SEARCH_MAX_RESULTS
        },
        "features": {
            "logging_enabled": ENABLE_LOGGING
        }
    }