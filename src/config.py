"""🏗️ Central configuration for MCP Template Server.

All settings and constants in one place for easy management.
"""

from __future__ import annotations

import os
from pathlib import Path

# =============================================================================
# 🚀 APPLICATION SETTINGS
# =============================================================================

APP_NAME = "MCP Template Server"
VERSION = "0.1.0"
DESCRIPTION = "🏗️ Template for building Model Context Protocol servers"
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

SERVER_NAME = "mcp-template"
SERVER_VERSION = VERSION

# =============================================================================
# ⏱️ TIMEOUTS AND LIMITS
# =============================================================================

DEFAULT_TIMEOUT = 30
CONNECTION_TIMEOUT = 10
MAX_RETRIES = 3
BATCH_SIZE = 50
CACHE_SIZE = 1000
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# =============================================================================
# 🎛️ FEATURE FLAGS
# =============================================================================

ENABLE_CACHE = True
ENABLE_LOGGING = True
ENABLE_DEBUG_LOGGING = DEBUG_MODE

# =============================================================================
# 📁 PATHS
# =============================================================================

BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# =============================================================================
# 🔧 TOOL SETTINGS
# =============================================================================

# Calculator
CALCULATOR_MAX_PRECISION = 15
CALCULATOR_ALLOWED_OPERATIONS = ["+", "-", "*", "/", "**", "%"]

# File manager
FILE_MANAGER_ALLOWED_EXTENSIONS = [".txt", ".json", ".md", ".py", ".yaml", ".yml"]
FILE_MANAGER_MAX_FILE_SIZE = MAX_FILE_SIZE
FILE_MANAGER_SAFE_DIRECTORIES = [str(DATA_DIR), str(ASSETS_DIR)]

# Search
SEARCH_MAX_RESULTS = 100
SEARCH_DEFAULT_LIMIT = 10
SEARCH_TIMEOUT = DEFAULT_TIMEOUT

# =============================================================================
# 📊 LOGGING
# =============================================================================

LOG_LEVEL = "DEBUG" if DEBUG_MODE else "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
LOG_FILE = LOGS_DIR / "mcp-server.log"

# =============================================================================
# 🔐 SECURITY
# =============================================================================

ALLOWED_READ_PATHS = [str(DATA_DIR), str(ASSETS_DIR)]
ALLOWED_WRITE_PATHS = [str(DATA_DIR)]
BLOCKED_EXTENSIONS = [".exe", ".bat", ".sh", ".cmd"]

MAX_STRING_LENGTH = 10000
MAX_LIST_LENGTH = 1000

# =============================================================================
# 🌍 ENVIRONMENT
# =============================================================================

def get_environment() -> str:
    """Get current environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    valid_envs = ["development", "staging", "production"]
    return env if env in valid_envs else "development"


def is_production() -> bool:
    """Check if running in production."""
    return get_environment() == "production"


def validate_config() -> None:
    """Validate configuration at startup."""
    required_settings = [APP_NAME, VERSION, SERVER_NAME]
    
    for setting in required_settings:
        if not setting:
            raise ValueError(f"❌ Missing required configuration: {setting}")
    
    if DEFAULT_TIMEOUT <= 0:
        raise ValueError("❌ DEFAULT_TIMEOUT must be positive")
    
    if MAX_RETRIES < 0:
        raise ValueError("❌ MAX_RETRIES must be non-negative")