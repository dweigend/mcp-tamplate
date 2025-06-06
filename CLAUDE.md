# 🤖 CLAUDE.md - LLM Development Instructions

This file contains specific instructions for AI assistants (Claude, GPT, etc.) working on this MCP Template project.

## 🎯 Project Overview

This is a **comprehensive template repository** for building Model Context Protocol (MCP) servers using Python and FastMCP. It provides:

- 🏗️ **Complete MCP architecture** with tools, resources, prompts, and API integrations
- 🔧 **Production-ready examples** of calculator, file manager, search tools, and data resources
- 💭 **LLM guidance system** with error handling and usage prompts
- 🧪 **Comprehensive testing** with pytest and 80%+ coverage
- 📊 **Enterprise-grade** configuration with logging, validation, and security
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
├── api/                # 🌐 External API integrations
│   └── web_search.py   # 🔍 Web search API client
├── prompts/            # 💭 MCP prompt templates for LLM guidance
│   ├── error_handling.py # 🚨 Troubleshooting guide
│   └── system_guide.py   # 📖 Server capabilities and usage examples
├── resources/          # 📊 Read-only data exposed to LLMs
│   ├── config_data.py  # ⚙️ Safe configuration data exposure
│   ├── health_status.py # 💚 Tool health monitoring data
│   └── server_info.py  # ℹ️ Server metadata and capabilities
└── tools/              # 🔧 Tool implementations (actions LLMs can invoke)
    ├── calculator.py   # 🧮 Math operations with validation
    ├── file_manager.py # 📁 Secure file operations (sandboxed)
    └── search.py       # 🔍 Web search integration
```

### 4. 🏛️ MCP Architecture Components

This template implements the full Model Context Protocol specification with four distinct layers:

#### 🔧 **Tools** (`src/tools/`)
Actions that LLMs can invoke to perform operations:
- **calculator.py**: Mathematical operations with input validation
- **file_manager.py**: Secure file operations within sandboxed directories  
- **search.py**: Web search integration using the API layer

#### 📊 **Resources** (`src/resources/`)
Read-only data that LLMs can access for context:
- **server_info.py**: Server metadata, version, capabilities, and uptime
- **health_status.py**: Real-time health monitoring of all components
- **config_data.py**: Safe subset of server configuration data

#### 💭 **Prompts** (`src/prompts/`)
Templates that guide LLM behavior and provide instructions:
- **system_guide.py**: Server capabilities and usage examples
- **error_handling.py**: Comprehensive troubleshooting guide for common errors

#### 🌐 **API Layer** (`src/api/`)
External service integrations and API clients:
- **web_search.py**: Mock web search API client (template for real integrations)

### 5. 🧪 Testing Requirements

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

### 6. 🔧 Adding New MCP Components

#### Adding New Tools
To add a new tool (action LLMs can invoke), follow this pattern:

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

#### Adding New Resources
To add a new resource (data LLMs can access):

1. **Create resource class** in `src/resources/new_resource.py`
2. **Implement data provider with health checks**
3. **Register in server** with `@mcp.resource()`
4. **Add tests** for data accuracy and performance

#### Adding New Prompts
To add a new prompt template:

1. **Create prompt provider** in `src/prompts/new_prompt.py`
2. **Define dynamic prompt generation logic**
3. **Register in server** with `@mcp.prompt()`
4. **Test prompt variations** and LLM responses

#### Adding New API Integrations
To add external service integration:

1. **Create API client** in `src/api/new_service.py`
2. **Implement authentication and error handling**
3. **Add configuration** for API keys and endpoints
4. **Mock in tests** to avoid external dependencies

### 7. 🛡️ Security Guidelines

- **Validate ALL inputs** using Pydantic models
- **Sanitize file paths** to prevent traversal attacks  
- **Restrict file operations** to allowed directories only
- **Limit resource usage** (file sizes, request counts, timeouts)
- **Never expose sensitive data** in responses or logs
- **Use safe defaults** and fail securely

### 8. 📊 Error Handling Patterns

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

### 9. 🔍 Code Quality Standards

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