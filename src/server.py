"""🚀 MCP Template Server - FastMCP Implementation.

Main server implementation using the Model Context Protocol Python SDK.
Provides tools, resources, and prompts for AI assistants like Claude.

References:
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- FastMCP Documentation: https://github.com/modelcontextprotocol/python-sdk#fastmcp
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
    ErrorDetail,
    FileManagerInput,
    FileManagerResult,
    HealthCheck,
    SearchQuery,
    SearchResponse,
    ServerInfo,
    ToolResponse,
)
from src.tools.calculator import CalculatorTool
from src.tools.file_manager import FileManagerTool
from src.tools.search import SearchTool

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
def calculate(input_data: CalculatorInput) -> ToolResponse:
    """🧮 Perform mathematical calculations with proper validation.
    
    Supports basic arithmetic operations with configurable precision.
    
    Args:
        input_data: Calculator input with operation type and numbers
        
    Returns:
        ToolResponse with calculation result or error details
        
    Example:
        >>> calculate(CalculatorInput(operation="add", numbers=[2, 3]))
        ToolResponse(success=True, data=CalculatorResult(...))
    """
    start_time = time.time()
    
    try:
        logger.info(f"🧮 Calculating: {input_data.operation} on {input_data.numbers}")
        
        result = calculator_tool.calculate(
            operation=input_data.operation,
            numbers=input_data.numbers,
            precision=input_data.precision or 2
        )
        
        execution_time = time.time() - start_time
        logger.info(f"✅ Calculation completed in {execution_time:.3f}s")
        
        return ToolResponse(
            success=True,
            data=result,
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        error_detail = ErrorDetail(
            code="CALCULATION_ERROR",
            message=str(e),
            details={"input": input_data.dict()},
            traceback=str(e) if DEBUG_MODE else None
        )
        
        logger.error(f"❌ Calculation failed: {e}")
        
        return ToolResponse(
            success=False,
            error=error_detail,
            execution_time=execution_time
        )


@mcp.tool()
def manage_file(input_data: FileManagerInput) -> ToolResponse:
    """📁 Perform secure file operations with validation.
    
    Supports reading, writing, listing, and checking file existence.
    All operations are sandboxed to allowed directories.
    
    Args:
        input_data: File manager input with operation and path
        
    Returns:
        ToolResponse with file operation result or error details
        
    Example:
        >>> manage_file(FileManagerInput(operation="read", path="data/example.txt"))
        ToolResponse(success=True, data=FileManagerResult(...))
    """
    start_time = time.time()
    
    try:
        logger.info(f"📁 File operation: {input_data.operation} on {input_data.path}")
        
        result = file_manager_tool.execute_operation(
            operation=input_data.operation,
            path=input_data.path,
            content=input_data.content,
            encoding=input_data.encoding
        )
        
        execution_time = time.time() - start_time
        logger.info(f"✅ File operation completed in {execution_time:.3f}s")
        
        return ToolResponse(
            success=True,
            data=result,
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        error_detail = ErrorDetail(
            code="FILE_OPERATION_ERROR",
            message=str(e),
            details={"input": input_data.dict()},
            traceback=str(e) if DEBUG_MODE else None
        )
        
        logger.error(f"❌ File operation failed: {e}")
        
        return ToolResponse(
            success=False,
            error=error_detail,
            execution_time=execution_time
        )


@mcp.tool()
def search_web(query: SearchQuery) -> ToolResponse:
    """🔍 Search the web with optional domain filtering.
    
    Performs web search with configurable limits and filters.
    Returns structured search results with relevance scoring.
    
    Args:
        query: Search query with text, domains, and limits
        
    Returns:
        ToolResponse with search results or error details
        
    Example:
        >>> search_web(SearchQuery(text="python tutorial", limit=5))
        ToolResponse(success=True, data=SearchResponse(...))
    """
    start_time = time.time()
    
    try:
        logger.info(f"🔍 Searching: '{query.text}' (limit: {query.limit})")
        
        results = search_tool.search(
            text=query.text,
            domains=query.domains,
            limit=query.limit,
            language=query.language
        )
        
        execution_time = time.time() - start_time
        logger.info(f"✅ Search completed in {execution_time:.3f}s, found {len(results.results)} results")
        
        return ToolResponse(
            success=True,
            data=results,
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        error_detail = ErrorDetail(
            code="SEARCH_ERROR",
            message=str(e),
            details={"query": query.dict()},
            traceback=str(e) if DEBUG_MODE else None
        )
        
        logger.error(f"❌ Search failed: {e}")
        
        return ToolResponse(
            success=False,
            error=error_detail,
            execution_time=execution_time
        )


# =============================================================================
# 📚 RESOURCES IMPLEMENTATION
# =============================================================================

@mcp.resource("server://info")
def get_server_info() -> ServerInfo:
    """⚙️ Get comprehensive server information and status.
    
    Returns detailed information about the MCP server including
    capabilities, uptime, and tool availability.
    
    Returns:
        ServerInfo: Complete server status and metadata
    """
    uptime = time.time() - server_start_time
    
    return ServerInfo(
        name=APP_NAME,
        version=VERSION,
        description="🏗️ Template for building Model Context Protocol servers",
        capabilities=[
            "mathematical_calculations",
            "file_operations", 
            "web_search",
            "health_monitoring"
        ],
        tools_count=3,  # calculate, manage_file, search_web
        uptime=uptime,
        status="running"
    )


@mcp.resource("server://health")
def get_health_status() -> HealthCheck:
    """💚 Comprehensive health check of server components.
    
    Performs health checks on all server subsystems and returns
    detailed status information.
    
    Returns:
        HealthCheck: Current health status and component checks
    """
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
    
    logger.info(f"💚 Health check completed: {status} ({response_time:.3f}s)")
    
    return HealthCheck(
        status=status,
        checks=checks,
        response_time=response_time
    )


@mcp.resource("config://settings") 
def get_configuration() -> Dict[str, Any]:
    """⚙️ Get current server configuration (safe subset).
    
    Returns non-sensitive configuration values that can be
    safely exposed to clients.
    
    Returns:
        Dict: Safe configuration settings
    """
    from src.config import (
        BATCH_SIZE,
        CACHE_SIZE,
        DEFAULT_TIMEOUT,
        MAX_RETRIES,
        SEARCH_DEFAULT_LIMIT,
        SEARCH_MAX_RESULTS,
    )
    
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


# =============================================================================
# 🎯 PROMPTS IMPLEMENTATION
# =============================================================================

@mcp.prompt()
def system_prompt() -> str:
    """🎯 System prompt for optimal MCP server interaction.
    
    Provides guidance for AI assistants on how to effectively
    use this MCP server's capabilities.
    
    Returns:
        str: Comprehensive system prompt
    """
    return f"""
🚀 {APP_NAME} v{VERSION} - MCP Server

You are connected to a powerful MCP server that provides:

🧮 **Calculator Tool**
- Perform mathematical operations (add, subtract, multiply, divide, power, modulo)
- Support for multiple numbers and configurable precision
- Usage: calculate(operation="add", numbers=[1, 2, 3], precision=2)

📁 **File Manager Tool**  
- Secure file operations within sandboxed directories
- Read, write, list, and check file existence
- Usage: manage_file(operation="read", path="data/example.txt")

🔍 **Search Tool**
- Web search with domain filtering and result limits
- Structured results with relevance scoring
- Usage: search_web(text="python tutorial", domains=["docs.python.org"], limit=5)

📊 **Server Resources**
- server://info - Get server information and status
- server://health - Comprehensive health check
- config://settings - Safe configuration values

💡 **Best Practices**
- Always validate inputs before making tool calls
- Use appropriate precision for calculations
- Specify file paths relative to allowed directories
- Filter search results by domain when possible
- Check server health if experiencing issues

🛡️ **Security**
- File operations are sandboxed to safe directories
- Path traversal protection is enforced
- Input validation prevents malicious requests
- Error handling provides safe failure modes

Use these tools efficiently to help users with calculations, file management, and information retrieval!
"""


@mcp.prompt()
def error_handling_guide() -> str:
    """🚨 Comprehensive error handling and troubleshooting guide.
    
    Provides detailed guidance on handling errors and edge cases
    when interacting with the MCP server.
    
    Returns:
        str: Error handling best practices
    """
    return """
🚨 MCP Server Error Handling Guide

**Common Error Types & Solutions:**

🧮 **Calculator Errors**
- Division by zero → Check second number is not 0
- Invalid operation → Use: add, subtract, multiply, divide, power, modulo
- Too many numbers → Some operations require exactly 2 numbers
- Precision out of range → Use 0-15 for precision value

📁 **File Operation Errors**
- Path not found → Ensure file exists in allowed directories (data/, assets/)
- Permission denied → Check file permissions and sandboxing rules
- Path traversal → Avoid '..' and absolute paths
- File too large → Files must be under 10MB
- Invalid encoding → Use utf-8 or specify correct encoding

🔍 **Search Errors**
- No results → Try broader search terms or remove domain filters
- Rate limiting → Wait before making additional requests
- Invalid domains → Ensure domain format includes TLD (e.g., example.com)
- Query too long → Keep search queries under 1000 characters

⚙️ **Server Errors**
- Resource unavailable → Check server health with server://health
- Timeout → Reduce request complexity or retry with backoff
- Configuration error → Verify server settings with config://settings

**Error Response Format:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {...},
    "timestamp": "2024-01-01T12:00:00"
  },
  "execution_time": 0.123
}
```

**Troubleshooting Steps:**
1. Check the error code and message
2. Verify input parameters match expected format
3. Test with simpler inputs to isolate the issue
4. Check server health if multiple operations fail
5. Review server logs for additional context (if available)

**Recovery Strategies:**
- Implement exponential backoff for retries
- Validate inputs before sending requests  
- Gracefully handle and display error messages to users
- Provide fallback options when operations fail
- Monitor server health proactively
"""


# =============================================================================
# 🏃‍♂️ SERVER STARTUP
# =============================================================================

def run_server() -> None:
    """🏃‍♂️ Start the MCP server with proper initialization."""
    logger.info(f"🚀 Starting {APP_NAME} v{VERSION}")
    logger.info(f"🔧 Debug mode: {DEBUG_MODE}")
    logger.info(f"📊 Logging enabled: {ENABLE_LOGGING}")
    
    try:
        # Validate configuration
        from src.config import validate_config
        validate_config()
        logger.info("✅ Configuration validated successfully")
        
        # Initialize tools
        logger.info("🔧 Initializing tools...")
        calculator_tool.initialize()
        file_manager_tool.initialize()
        search_tool.initialize()
        logger.info("✅ All tools initialized successfully")
        
        # Start server
        logger.info(f"🌐 MCP Server ready at {SERVER_NAME}")
        mcp.run()
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise


if __name__ == "__main__":
    run_server()