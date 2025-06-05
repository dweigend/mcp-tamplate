"""🚨 Error Handling Guide - Example implementation."""


def get_error_handling_guide() -> str:
    """Comprehensive error handling and troubleshooting guide."""
    return """
🚨 MCP Template Error Handling Guide

**Common Error Types & Solutions:**

🧮 **Calculator Errors (Example Tool)**
- Division by zero → Check second number is not 0
- Invalid operation → Use: add, subtract, multiply, divide, power, modulo
- Too many numbers → Some operations require exactly 2 numbers
- Precision out of range → Use 0-15 for precision value

📁 **File Operation Errors (Example Tool)**
- Path not found → Ensure file exists in allowed directories (data/, assets/)
- Permission denied → Check file permissions and sandboxing rules
- Path traversal → Avoid '..' and absolute paths
- File too large → Files must be under 10MB
- Invalid encoding → Use utf-8 or specify correct encoding

🔍 **Search Errors (Example Tool - Mock Implementation)**
- No results → This is a mock implementation for template purposes
- Rate limiting → Simulated in example implementation
- Invalid domains → Example validation patterns
- Query too long → Example length limits

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

**Template Implementation Notes:**
- All tools are examples demonstrating patterns
- Replace with real implementations for production
- Error handling shows best practices for MCP servers
- Security patterns prevent common vulnerabilities

**Recovery Strategies:**
- Implement exponential backoff for retries
- Validate inputs before sending requests  
- Gracefully handle and display error messages to users
- Provide fallback options when operations fail
- Monitor server health proactively
"""