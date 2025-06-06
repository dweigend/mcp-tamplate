# 📊 MCP Resources

Read-only data exposed to LLMs for context and information.

## What are MCP Resources?

Application-controlled data that LLMs can access.

📖 **See MCP Documentation**: https://modelcontextprotocol.io/docs/concepts/resources

## Current Files

- `server_info.py` - Server metadata and capabilities
- `health_status.py` - Tool health monitoring
- `config_data.py` - Safe configuration exposure

## Pattern

```python
def get_resource_data() -> Dict[str, Any]:
    """Return structured data for LLM access."""
    return {
        "key": "value",
        "timestamp": datetime.now()
    }
```