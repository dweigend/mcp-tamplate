# 🌐 API Directory

External API integrations for the MCP server.

## Purpose

Isolates external service integrations from MCP logic:
- Web search APIs
- Third-party services
- Mock implementations for testing

## Current Files

- `web_search.py` - Example web search API client (mock implementation)

## Pattern

```python
class APIClient:
    def __init__(self, api_key=None):
        self._api_key = api_key
    
    def health_check(self) -> bool:
        # Test connectivity
        pass
    
    def search(self, query: str) -> List[Dict]:
        # API request logic
        pass
```