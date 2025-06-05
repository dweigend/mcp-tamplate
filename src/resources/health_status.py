"""💚 Health Status Resource - Example implementation."""

import logging
import time
from typing import Any, Dict

from src.config import ENABLE_LOGGING


def get_health_status(calculator_tool, file_manager_tool, search_tool) -> Dict[str, Any]:
    """Comprehensive health check of server components."""
    start_time = time.time()
    
    # Perform health checks
    checks = {
        "server_running": True,
        "tools_available": True,
        "file_system_accessible": file_manager_tool.health_check(),
        "calculator_functional": calculator_tool.health_check(),
        "search_available": search_tool.health_check(),
        "logging_working": ENABLE_LOGGING
    }
    
    # Determine overall status
    all_healthy = all(checks.values())
    status = "healthy" if all_healthy else "degraded"
    
    response_time = time.time() - start_time
    
    logger = logging.getLogger(__name__)
    logger.info(f"💚 Health check completed: {status} ({response_time:.3f}s)")
    
    return {
        "status": status,
        "checks": checks,
        "response_time": response_time
    }