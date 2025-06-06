# 🏗️ Source Code Directory

Core implementation of the MCP Template Server.

## 📁 Structure

```
src/
├── config.py              # 🎛️ Central configuration and settings
├── models.py              # 📊 Pydantic data models and validation
├── server.py              # 🚀 FastMCP server implementation
├── api/                   # 🌐 External API integrations
│   └── web_search.py      # 🔍 Web search API client
├── prompts/               # 💬 System prompts and guides
│   ├── error_handling.py  # ❌ Error handling prompts
│   └── system_guide.py    # 📖 System guide prompts
├── resources/             # 📊 MCP resources
│   ├── config_data.py     # ⚙️ Configuration data resource
│   ├── health_status.py   # 💚 Health status resource
│   └── server_info.py     # ℹ️ Server information resource
└── tools/                 # 🔧 Tool implementations
    ├── calculator.py      # 🧮 Mathematical operations
    ├── file_manager.py    # 📁 Secure file operations
    └── search.py          # 🔍 Search functionality
```

## 🎛️ Configuration (`config.py`)

Central configuration management following the principle of **centralized settings**.

**Key Features:**
- Environment-based configuration
- Feature flags for development/production
- Path management with automatic directory creation
- Security settings and validation

**Usage:**
```python
from src.config import DEBUG_MODE, DATA_DIR, validate_config

# Always validate config at startup
validate_config()
```

## 📊 Data Models (`models.py`)

Pydantic models for type-safe data validation and serialization.

**Key Principles:**
- Simplified field definitions
- Built-in validation logic
- Early returns in validators
- Clear error messages

**Example:**
```python
from src.models import CalculatorInput, OperationType

calc_input = CalculatorInput(
    operation=OperationType.ADD,
    numbers=[2.0, 3.0],
    precision=2
)
```

## 🚀 Server Implementation (`server.py`)

FastMCP server with tools, resources, and prompts.

**Architecture:**
- Async/await patterns
- Decorator-based registration
- Comprehensive error handling
- Structured logging

**Adding New Tools:**
```python
@mcp.tool()
def your_tool(input_data: YourModel) -> ToolResponse:
    # Implementation with validation and error handling
    pass
```

## 🔧 Tools Directory

Individual tool implementations following single responsibility principle.

### 🧮 Calculator (`tools/calculator.py`)
- Mathematical operations with validation
- Configurable precision
- Division by zero protection
- Type-safe decimal arithmetic

### 📁 File Manager (`tools/file_manager.py`)
- Sandboxed file operations
- Path traversal protection
- Encoding support
- Size limit enforcement

### 🔍 Search (`tools/search.py`)
- Mock search implementation
- Domain filtering
- Rate limiting
- Extensible for real APIs

## 🌐 API Directory

External API integrations and clients.

### 🔍 Web Search API (`api/web_search.py`)
- Example API client implementation
- Configurable API key support
- Health check functionality
- Mock search results for testing
- Ready to replace with real search APIs (Google, Bing, etc.)

## 💬 Prompts Directory

System prompts and guidance for optimal MCP interaction.

### ❌ Error Handling Guide (`prompts/error_handling.py`)
- Comprehensive error documentation
- Tool-specific error solutions
- Common troubleshooting patterns
- User-friendly error messages

### 📖 System Guide (`prompts/system_guide.py`)
- Server introduction and capabilities
- Tool documentation and examples
- Usage patterns and best practices
- Version and feature information

## 📊 Resources Directory

MCP resources for server information and monitoring.

### ⚙️ Configuration Data (`resources/config_data.py`)
- Safe exposure of server settings
- Runtime configuration values
- Feature flags and limits
- No sensitive data exposure

### 💚 Health Status (`resources/health_status.py`)
- Comprehensive health checks
- Tool availability monitoring
- Performance timing metrics
- Real-time status reporting

### ℹ️ Server Information (`resources/server_info.py`)
- Server metadata and version
- Capability discovery
- Uptime tracking
- Feature documentation

## 🔄 Development Patterns

### Adding New Tools

1. **Create the tool class:**
```python
class YourTool:
    def __init__(self) -> None:
        self._initialized = False
    
    def initialize(self) -> None:
        # Setup code
        self._initialized = True
    
    def health_check(self) -> bool:
        # Health validation
        return True
    
    def execute_operation(self, input_data) -> YourResult:
        # Main functionality
        pass
```

2. **Add server integration:**
```python
@mcp.tool()
def your_tool_function(input_data: YourModel) -> ToolResponse:
    # Server wrapper with timing and error handling
    pass
```

3. **Create comprehensive tests:**
```python
class TestYourTool:
    def test_basic_operation(self):
        # Test implementation
        pass
```

### Coding Standards

- **Functions:** Max 20 lines
- **Nesting:** Max 2 levels deep
- **Validation:** Early returns with clear errors
- **Logging:** Structured with appropriate levels
- **Types:** Full type hints for all functions
- **Tests:** 80%+ coverage with edge cases

### Error Handling

```python
def your_function(data: InputModel) -> OutputModel:
    if not data:
        return create_error_response("Data required")
    
    if not validate_data(data):
        logger.warning("Invalid data provided")
        return create_error_response("Invalid data format")
    
    # Main processing logic
    return create_success_response(result)
```

## 🧪 Testing

Each component has corresponding tests in `tests/`:

```bash
# Run all tests
uv run pytest

# Test specific component
uv run pytest tests/test_tools.py::TestCalculatorTool -v

# Coverage report
uv run pytest --cov=src --cov-report=html
```

## 📚 Documentation

- **Inline:** Minimal docstrings for complex functions only
- **Types:** Self-documenting through type hints
- **Examples:** In docstrings for non-obvious usage
- **Architecture:** High-level patterns documented here

## 🔒 Security

- **Input Validation:** All data validated with Pydantic
- **Path Security:** No traversal attacks allowed
- **Resource Limits:** File sizes, timeouts, etc.
- **Error Handling:** No sensitive data in error messages

## 🚀 Performance

- **Async Operations:** Where beneficial
- **Caching:** Configurable for expensive operations
- **Resource Management:** Proper cleanup and limits
- **Profiling:** Built-in context managers available