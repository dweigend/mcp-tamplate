"""⚙️ Server Information Resource - Example implementation."""

import time
from typing import Any, Dict

from src.config import APP_NAME, VERSION


def get_server_info(start_time: float) -> Dict[str, Any]:
    """Get comprehensive server information and status."""
    uptime = time.time() - start_time
    
    return {
        "name": APP_NAME,
        "version": VERSION,
        "description": "🔧 Template for building Model Context Protocol servers with example tools",
        "capabilities": [
            "mathematical_calculations",
            "file_operations", 
            "web_search",
            "health_monitoring"
        ],
        "tools_count": 3,  # calculate, manage_file, search_web
        "uptime": uptime,
        "status": "running"
    }