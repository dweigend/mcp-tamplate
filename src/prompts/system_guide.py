"""🎯 System Prompt - Example implementation."""

from src.config import APP_NAME, VERSION


def get_system_prompt() -> str:
    """System prompt for optimal MCP server interaction."""
    return f"""
🔧 {APP_NAME} v{VERSION} - Example MCP Server

You are connected to a template MCP server that demonstrates:

🧮 **Calculator Tool (Example)**
- Mathematical operations with validation
- Usage: calculate(operation="add", numbers=[1, 2, 3], precision=2)

📁 **File Manager Tool (Example)**  
- Secure file operations within sandboxed directories
- Usage: manage_file(operation="read", path="data/example.txt")

🔍 **Search Tool (Example - Mock Implementation)**
- Web search patterns with domain filtering
- Usage: search_web(text="tutorial", domains=["example.com"], limit=5)

📊 **Server Resources**
- server://info - Get server information and status
- server://health - Comprehensive health check
- config://settings - Safe configuration values

⚠️ **Important**: These are **example tools** demonstrating MCP patterns. 
Replace with your own implementations for production use.

💡 **Best Practices**
- Always validate inputs before making tool calls
- Use appropriate precision for calculations
- Specify file paths relative to allowed directories
- Check server health if experiencing issues

🛡️ **Security Features**
- Input validation with Pydantic models
- Sandboxed file operations
- Path traversal protection
- Safe error handling

This template shows you how to structure MCP servers. Customize and extend it for your specific use case!
"""