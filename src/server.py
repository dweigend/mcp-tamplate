"""🚀 MCP Template Server - Clean Architecture Implementation.

Main server implementation using FastMCP with separated concerns:
- Tools: Executable functionality for LLMs  
- Resources: Data access and server information
- Prompts: Reusable interaction templates
- API Layer: External service integrations

This demonstrates MCP best practices and clean architecture patterns.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from src.config import (
    APP_NAME,
    DEBUG_MODE,
    ENABLE_LOGGING,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    SERVER_NAME,
    VERSION,
)
from src.models import (
    CalculatorInput,
    CalculatorResult,
    FileManagerInput,
    FileManagerResult,
    SearchQuery,
    SearchResponse,
)
from src.tools.calculator import CalculatorTool
from src.tools.file_manager import FileManagerTool
from src.tools.search import SearchTool
from src.resources.server_info import get_server_info
from src.resources.health_status import get_health_status
from src.resources.config_data import get_safe_configuration
from src.prompts.system_guide import get_system_prompt
from src.prompts.error_handling import get_error_handling_guide

# =============================================================================
# 📊 LOGGING SETUP
# =============================================================================

def setup_logging() -> logging.Logger:
    """📊 Configure structured logging for the MCP server."""
    logger = logging.getLogger(SERVER_NAME)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler (if logging enabled)
    if ENABLE_LOGGING:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    if ENABLE_LOGGING:
        file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    if ENABLE_LOGGING:
        logger.addHandler(file_handler)
    
    return logger


# =============================================================================
# 🚀 MCP SERVER INITIALIZATION
# =============================================================================

# Initialize FastMCP server
mcp = FastMCP(SERVER_NAME)
logger = setup_logging()
server_start_time = time.time()

# Initialize tool instances
calculator_tool = CalculatorTool()
file_manager_tool = FileManagerTool()
search_tool = SearchTool()


# =============================================================================
# 🔧 TOOLS IMPLEMENTATION
# =============================================================================

@mcp.tool()
def calculate(operation: str, numbers: List[float], precision: int = 2) -> CalculatorResult:
    """🧮 Perform mathematical calculations with proper validation.
    
    Example tool demonstrating mathematical operations with validation.
    
    Args:
        operation: Mathematical operation (add, subtract, multiply, divide, power, modulo)
        numbers: List of numbers to operate on (1-10 numbers)
        precision: Decimal precision for result (0-15, default: 2)
        
    Returns:
        CalculatorResult with calculation details
    """
    logger.info(f"🧮 Calculating: {operation} on {numbers}")
    
    # Create input model for validation
    calc_input = CalculatorInput(
        operation=operation,
        numbers=numbers,
        precision=precision
    )
    
    # Perform calculation
    result = calculator_tool.calculate(
        operation=calc_input.operation,
        numbers=calc_input.numbers,
        precision=calc_input.precision
    )
    
    logger.info(f"✅ Calculation completed: {result.formatted_result}")
    return result


@mcp.tool()
def manage_file(
    operation: str, 
    path: str, 
    content: Optional[str] = None, 
    encoding: str = "utf-8"
) -> FileManagerResult:
    """📁 Perform secure file operations with validation.
    
    Example tool demonstrating secure file operations within sandboxed directories.
    
    Args:
        operation: File operation (read, write, list, exists, delete)
        path: File path relative to allowed directories
        content: Content for write operations (optional)
        encoding: File encoding (default: utf-8)
        
    Returns:
        FileManagerResult with operation details
    """
    logger.info(f"📁 File operation: {operation} on {path}")
    
    # Create input model for validation
    file_input = FileManagerInput(
        operation=operation,
        path=path,
        content=content,
        encoding=encoding
    )
    
    # Perform file operation
    result = file_manager_tool.execute_operation(
        operation=file_input.operation,
        path=file_input.path,
        content=file_input.content,
        encoding=file_input.encoding
    )
    
    logger.info(f"✅ File operation completed: {result.message}")
    return result


@mcp.tool()
def search_web(
    text: str, 
    domains: Optional[List[str]] = None, 
    limit: int = 10, 
    language: str = "en"
) -> SearchResponse:
    """🔍 Search the web with optional domain filtering.
    
    Example tool demonstrating web search patterns (mock implementation).
    
    Args:
        text: Search query text (1-1000 characters)
        domains: Optional domain filters (max 10)
        limit: Maximum results to return (1-100, default: 10)
        language: Search language (default: en)
        
    Returns:
        SearchResponse with search results
    """
    logger.info(f"🔍 Searching: '{text}' (limit: {limit})")
    
    # Create query model for validation
    search_query = SearchQuery(
        text=text,
        domains=domains or [],
        limit=limit,
        language=language
    )
    
    # Perform search
    results = search_tool.search(
        text=search_query.text,
        domains=search_query.domains,
        limit=search_query.limit,
        language=search_query.language
    )
    
    logger.info(f"✅ Search completed, found {len(results.results)} results")
    return results


# =============================================================================
# 📚 RESOURCES IMPLEMENTATION
# =============================================================================

@mcp.resource("server://info")
def server_info() -> str:
    """⚙️ Get comprehensive server information and status."""
    info = get_server_info(server_start_time)
    return f"""
# Server Information

**Name:** {info['name']}
**Version:** {info['version']}
**Description:** {info['description']}
**Status:** {info['status']}
**Uptime:** {info['uptime']:.1f} seconds
**Tools Available:** {info['tools_count']}

**Capabilities:**
{chr(10).join(f"- {cap}" for cap in info['capabilities'])}

This is an example MCP server template demonstrating tools, resources, and prompts.
"""


@mcp.resource("server://health")
def health_status() -> str:
    """💚 Comprehensive health check of server components."""
    health = get_health_status(calculator_tool, file_manager_tool, search_tool)
    
    status_emoji = "💚" if health['status'] == "healthy" else "🔴"
    checks_list = []
    for check_name, check_status in health['checks'].items():
        emoji = "✅" if check_status else "❌"
        checks_list.append(f"{emoji} {check_name.replace('_', ' ').title()}")
    
    return f"""
# Health Status {status_emoji}

**Overall Status:** {health['status'].upper()}
**Response Time:** {health['response_time']:.3f}s

**Component Checks:**
{chr(10).join(checks_list)}
"""


@mcp.resource("config://settings") 
def configuration() -> str:
    """⚙️ Get current server configuration (safe subset)."""
    config = get_safe_configuration()
    return f"""
# Server Configuration

## Server
- Name: {config['server']['name']}
- Version: {config['server']['version']}
- Debug Mode: {config['server']['debug_mode']}

## Limits
- Default Timeout: {config['limits']['default_timeout']}s
- Max Retries: {config['limits']['max_retries']}
- Batch Size: {config['limits']['batch_size']}
- Cache Size: {config['limits']['cache_size']}

## Search Settings
- Default Limit: {config['search']['default_limit']}
- Max Results: {config['search']['max_results']}

## Features
- Logging Enabled: {config['features']['logging_enabled']}
"""


# =============================================================================
# 🎯 PROMPTS IMPLEMENTATION
# =============================================================================

@mcp.prompt()
def system_prompt() -> str:
    """🎯 System prompt for optimal MCP server interaction."""
    return get_system_prompt()


@mcp.prompt()
def error_handling_guide() -> str:
    """🚨 Comprehensive error handling and troubleshooting guide."""
    return get_error_handling_guide()


# =============================================================================
# 🏃‍♂️ SERVER STARTUP
# =============================================================================

def _initialize_tools() -> None:
    """Initialize all tools."""
    calculator_tool.initialize()
    file_manager_tool.initialize()
    search_tool.initialize()


def run_server() -> None:
    """🏃‍♂️ Start the MCP server with proper initialization."""
    logger.info(f"🚀 Starting {APP_NAME} v{VERSION}")
    
    try:
        # Validate configuration
        from src.config import validate_config
        validate_config()
        logger.info("✅ Configuration validated")
        
        # Initialize tools
        _initialize_tools()
        logger.info("✅ Tools initialized")
        
        # Start server
        logger.info(f"🌐 MCP Server ready at {SERVER_NAME}")
        mcp.run()
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise


if __name__ == "__main__":
    run_server()