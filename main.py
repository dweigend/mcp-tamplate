"""🚀 MCP Template Server - Main Entry Point.

Production entry point for the Model Context Protocol server.
Handles server initialization, configuration validation, and startup.

Usage:
    python main.py                    # Start server with default settings
    DEBUG=true python main.py         # Start with debug logging
    ENVIRONMENT=production python main.py  # Production mode

References:
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Server configuration: src/config.py
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.server import run_server
from src.config import (
    APP_NAME,
    VERSION,
    DEBUG_MODE,
    get_environment,
    validate_config,
)

# Configure basic logging for startup
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main() -> None:
    """🚀 Main entry point for MCP Template Server."""
    try:
        # Print startup banner
        print(f"""
🏗️ {APP_NAME} v{VERSION}
🌍 Environment: {get_environment()}
🔧 Debug Mode: {DEBUG_MODE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        logger.info(f"🚀 Starting {APP_NAME} v{VERSION}")
        logger.info(f"🌍 Environment: {get_environment()}")
        
        # Validate configuration
        validate_config()
        logger.info("✅ Configuration validated")
        
        # Start MCP server
        run_server()
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        if DEBUG_MODE:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()