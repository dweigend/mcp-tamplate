# 🤖 CLAUDE.md - LLM Development Instructions

This file contains specific instructions for AI assistants (Claude, GPT, etc.) working on this MCP Template project.

## 🎯 Project Overview

This is a **template repository** for building Model Context Protocol (MCP) servers using Python and FastMCP. It provides:

- 🏗️ **Structured architecture** with tools, resources, and prompts
- 🔧 **Example implementations** of calculator, file manager, and search tools  
- 🧪 **Comprehensive testing** with pytest and 80%+ coverage
- 📊 **Production-ready** configuration with logging, validation, and security
- 🚀 **Easy deployment** with UV package management and CLI tools

## 🔄 Development Workflow

When working on this project, follow these principles:

### 1. 📖 Always Read First
```bash
# Before making changes, understand the current state
uv run python cli.py health         # Check tool health
uv run python cli.py demo          # See current functionality  
uv run pytest                      # Run tests
uv run ruff check                   # Check code quality
```

### 2. 🏗️ Architecture Principles

- **Central Configuration**: All settings in `src/config.py`
- **Single Responsibility**: Each tool does one thing well  
- **Early Returns**: Validate inputs first, handle errors gracefully
- **Type Safety**: Use Pydantic models for all data structures
- **Security First**: Sandbox file operations, validate all inputs
- **Self-Documenting**: Clear names, minimal but helpful docstrings

### 3. 📁 File Organization

```
src/
├── config.py           # 🎛️ ALL configuration settings
├── models.py           # 📊 Pydantic data models  
├── server.py           # 🚀 FastMCP server implementation
└── tools/              # 🔧 Tool implementations
    ├── calculator.py   # 🧮 Math operations
    ├── file_manager.py # 📁 Secure file operations
    └── search.py       # 🔍 Web search (mock implementation)
```

### 4. 🧪 Testing Requirements

- **Minimum 80% code coverage**
- **Test all error paths** and edge cases
- **Use fixtures** for setup/teardown
- **Mock external dependencies** (APIs, file system)
- **Performance tests** for critical operations

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test categories  
uv run pytest -m integration       # Integration tests
uv run pytest -m performance       # Performance tests
uv run pytest tests/test_models.py # Model validation tests
```

### 5. 🔧 Adding New Tools

To add a new tool, follow this pattern:

1. **Create model classes** in `src/models.py`:
```python
class NewToolInput(BaseModel):
    parameter: str = Field(..., description="Parameter description")

class NewToolResult(BaseModel):
    result: str = Field(..., description="Result description")
```

2. **Implement tool class** in `src/tools/new_tool.py`:
```python
class NewTool:
    def __init__(self) -> None:
        self._initialized = False
    
    def initialize(self) -> None:
        # Setup code here
        self._initialized = True
    
    def health_check(self) -> bool:
        # Health check logic
        return True
    
    def execute_operation(self, input_data: NewToolInput) -> NewToolResult:
        # Main tool logic with validation and error handling
        pass
```

3. **Add server integration** in `src/server.py`:
```python
@mcp.tool()
def new_tool_function(input_data: NewToolInput) -> ToolResponse:
    # Server wrapper with error handling and timing
    pass
```

4. **Create comprehensive tests** in `tests/test_tools.py`
5. **Update CLI** in `cli.py` for local testing
6. **Add configuration** to `src/config.py` if needed

### 6. 🛡️ Security Guidelines

- **Validate ALL inputs** using Pydantic models
- **Sanitize file paths** to prevent traversal attacks  
- **Restrict file operations** to allowed directories only
- **Limit resource usage** (file sizes, request counts, timeouts)
- **Never expose sensitive data** in responses or logs
- **Use safe defaults** and fail securely

### 7. 📊 Error Handling Patterns

```python
# ✅ Good: Early returns with validation
def process_data(data: InputModel) -> Result:
    if not data:
        raise ValueError("Data required")
    
    if not validate_data(data):
        logger.warning("Invalid data provided")
        return create_error_response("Invalid data")
    
    # Main processing logic
    return create_success_response(result)

# ❌ Bad: Nested error handling
def process_data(data):
    try:
        if data:
            try:
                result = complex_operation(data)
                return result
            except ProcessingError:
                return handle_error()
    except ValidationError:
        return handle_validation_error()
```

### 8. 🔍 Code Quality Standards

- **Line length**: 120 characters maximum
- **Function length**: 20 lines maximum  
- **Nesting depth**: 2 levels maximum
- **Type hints**: Required for all functions
- **Docstrings**: One-line for simple functions, detailed for complex ones
- **Variable names**: Clear and self-documenting

```bash
# Code quality checks
uv run ruff check --fix .    # Fix auto-fixable issues
uv run ruff format .         # Format code  
uv run mypy src/             # Type checking
```

## 🚀 Deployment Checklist

Before deploying or sharing code:

- [ ] ✅ All tests pass (`uv run pytest`)
- [ ] 🧹 Code passes linting (`uv run ruff check`)
- [ ] 📊 80%+ test coverage
- [ ] 💚 Health checks pass (`uv run python cli.py health`)
- [ ] 🔒 Security review (no exposed secrets, safe file operations)
- [ ] 📝 Documentation updated
- [ ] 🎯 Demo works (`uv run python cli.py demo`)

## 🎯 Integration with Claude Desktop

To use this MCP server with Claude Desktop:

1. **Start the server**:
```bash
uv run python main.py
```

2. **Add to Claude Desktop config**:
```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/mcp-template"
    }
  }
}
```

3. **Test the connection** in Claude Desktop

## 🔧 Common Development Tasks

### Adding Dependencies
```bash
uv add package-name              # Add runtime dependency
uv add --dev package-name        # Add development dependency
```

### Local Testing
```bash
uv run python cli.py interactive  # Interactive testing mode
uv run python cli.py calculate add 2 3  # Direct tool testing
uv run python cli.py health       # Health check
```

### Performance Profiling
```bash
# Use the built-in profiling context manager
with ProfileContext("Operation Name"):
    expensive_operation()
```

### Debugging
```bash
DEBUG=true uv run python main.py  # Start with debug logging
uv run python cli.py --json       # Get JSON output for analysis
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're using `uv run` and paths are correct
2. **File Permission Errors**: Check that data/ directory exists and is writable  
3. **Test Failures**: Run `uv run pytest -v` for verbose output
4. **Linting Errors**: Run `uv run ruff check --fix .` to auto-fix issues

### Getting Help

1. Check existing tests for usage examples
2. Use `uv run python cli.py --help` for CLI usage
3. Review `src/config.py` for configuration options
4. Look at Pydantic model definitions in `src/models.py`

## 📋 Code Templates

### New Tool Template
```python
"""🔧 New Tool - Brief Description.

Detailed description of what this tool does.
"""

from __future__ import annotations
import logging
from src.models import BaseModel, ToolResponse
from src.config import TOOL_SPECIFIC_SETTINGS

logger = logging.getLogger(__name__)

class NewTool:
    def __init__(self) -> None:
        self._initialized = False
    
    def initialize(self) -> None:
        if self._initialized:
            return
        # Initialization logic
        self._initialized = True
        logger.info("🔧 New tool initialized")
    
    def health_check(self) -> bool:
        try:
            # Health check logic
            return True
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False
    
    def execute_operation(self, input_data) -> ToolResponse:
        if not self._initialized:
            self.initialize()
        
        # Validation
        # Processing  
        # Error handling
        # Return structured response
        pass
```

### Test Template
```python
"""🧪 Tests for New Tool."""

import pytest
from src.tools.new_tool import NewTool

class TestNewTool:
    @pytest.fixture
    def tool(self):
        tool = NewTool()
        tool.initialize()
        return tool
    
    def test_initialization(self):
        tool = NewTool()
        assert not tool._initialized
        tool.initialize()
        assert tool._initialized
    
    def test_health_check(self, tool):
        assert tool.health_check() is True
    
    def test_basic_operation(self, tool):
        # Test successful operation
        pass
    
    def test_error_handling(self, tool):
        # Test error cases
        pass
```

Remember: This is a **template project** meant to be copied and customized. Focus on creating clean, well-tested, secure code that others can easily understand and extend! 🚀