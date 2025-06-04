# 🏄‍♂️ Windsurf Rules - Perplexity MCP Server

## 🎛️ Coding Standards

- Write self-documenting code with clear variable and function names
- Use line length of 120 characters max
- Keep functions under 20 lines
- Maximum nesting depth of 2 levels
- Prefer flat code structure over nested conditionals
- One responsibility per function
- Export one thing per file

## 📦 Development Tools

- Use `uv add <package>` for adding dependencies
- Use `uv run` to execute scripts
- Configure tools in pyproject.toml:
  ```toml
  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"

  [tool.ruff]
  line-length = 120
  target-version = "py311"
  select = ["E", "F", "I", "N", "UP"]

  [tool.ruff.format]
  quote-style = "double"
  indent-style = "space"
  ```

## 📝 Documentation

- Use minimal one-line docstrings for functions
- Document only what's not obvious from function/variable names
- Comment only to explain "why" not "what" or "how"
- Prefer clear code over extensive documentation

## ✅ Code Patterns To Use

```python
# Pydantic models for validation
class SearchQuery(BaseModel):
    """Query with optional domain filters."""
    text: str
    domains: list[str] = []
    limit: int = 10

# Lookup tables over if-chains
STATUS_HANDLERS = {
    "error": handle_error,
    "success": handle_success,
    "pending": handle_pending,
}

# Early returns over nested conditionals
def validate(data):
    if not data:
        return False
    if data.is_expired:
        return False
    return True

# Context managers for resources
async with AsyncClient() as client:
    response = await client.get(url)
```

## ❌ Patterns To Avoid

```python
# Avoid: Deep nesting
def process(data):
    if data:
        if data.is_valid:
            if data.has_permission:
                # Logic buried 3 levels deep
                pass

# Avoid: Long parameter lists
def search(query, filters, limit, offset, sort_by, order, timeout, retry):
    pass  # Use a model or dataclass instead

# Avoid: Magic numbers/strings
if status_code == 403:  # What's 403?
    handle_unauthorized()
```

## 🗂️ Organization Principles

- Group code by feature, not by type
- Keep related functionality together
- Core modules should not import from peripheral ones
- High-level modules define interfaces, low-level modules implement them
- Each component should function independently
- Place related files close to each other

## 🔍 Data Validation

- Use Pydantic for all data validation
- Create model hierarchies for complex data
- Use Field validators for complex validations
- Use BaseSettings for configuration

## 💾 Storage Best Practices

- Use TinyDB tables for different data types
- Cache frequent queries using lru_cache
- Add timestamps to documents using middleware
- Use transactions for multiple operations

## 🔄 API Patterns

- Create thin API client functions that return structured data
- Handle exceptions and wrap in consistent response format
- Return structured responses with status field
- Implement rate limiting and backoff for external APIs

## 🧪 Error Handling

- Create custom exception hierarchy
- Use descriptive error messages
- Return structured error responses
- Implement graceful degradation for API failuress
