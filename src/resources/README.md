# 📁 Example Resources

> These are demonstration MCP resources showing how to expose data to LLMs.

## Purpose

Resources provide **application-controlled** data access:
- Server information and status
- Configuration data (safe subset)
- Dynamic content and metadata
- File contents and system data

## MCP Resource Pattern

Resources are identified by URI and provide either:
- **Text content** (UTF-8 encoded)
- **Binary content** (base64 encoded)

## Example Structure

```
resources/
├── README.md           # This file
├── server_info.py      # Server metadata resource
├── health_status.py    # Health monitoring resource  
└── config_data.py      # Configuration resource
```

## Implementation Pattern

```python
@mcp.resource("scheme://path")
def resource_handler() -> ResourceData:
    # Return structured data for LLM consumption
    pass
```