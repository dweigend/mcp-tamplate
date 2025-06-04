# 🏗️ MCP Template Server

A production-ready template for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers with Python and FastMCP.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-1.0+-green.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## ✨ Features

- 🚀 **Production Ready**: Comprehensive error handling, logging, and validation
- 🔧 **Example Tools**: Calculator, file manager, and search implementations
- 🧪 **Comprehensive Testing**: 80%+ test coverage with pytest
- 🔒 **Security First**: Input validation, sandboxing, and safe file operations
- 📊 **Observability**: Health checks, metrics, and structured logging
- 🛠️ **Developer Experience**: CLI testing tool, hot reload, and clear documentation
- 🎯 **Type Safe**: Full Pydantic integration with validation
- ⚡ **Fast**: Built on FastMCP for optimal performance

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the template**:
```bash
git clone https://github.com/yourusername/mcp-template.git
cd mcp-template
```

2. **Install dependencies**:
```bash
uv sync
```

3. **Run health check**:
```bash
uv run python cli.py health
```

4. **Start the MCP server**:
```bash
uv run python main.py
```

5. **Test tools locally**:
```bash
uv run python cli.py demo
```

## 🔧 Available Tools

### 🧮 Calculator Tool
Perform mathematical operations with proper validation and configurable precision.

```bash
# CLI Usage
uv run python cli.py calculator calculate add 2 3 5
uv run python cli.py calculator calculate divide 10 3 --precision 4
```

**Features:**
- Basic arithmetic (add, subtract, multiply, divide)
- Advanced operations (power, modulo)
- Configurable decimal precision (0-15)
- Input validation and error handling
- Division by zero protection

### 📁 File Manager Tool
Secure file operations with sandboxing and validation.

```bash
# CLI Usage  
uv run python cli.py file write data/test.txt "Hello, World!"
uv run python cli.py file read data/test.txt
uv run python cli.py file list data/
```

**Features:**
- Read, write, list, delete, and check file operations
- Path traversal protection
- File size limits and validation
- Encoding support with fallbacks
- Sandboxed to safe directories only

### 🔍 Search Tool
Web search with domain filtering and structured results.

```bash
# CLI Usage
uv run python cli.py search web "python tutorial" --limit 5
uv run python cli.py search web "API docs" -d docs.python.org -d github.com
```

**Features:**
- Configurable result limits (1-100)
- Domain filtering for targeted results
- Language support
- Relevance scoring
- Rate limiting protection
- Mock implementation (integrate with real APIs)

## 📚 Server Resources

Access server information and configuration through MCP resources:

- `server://info` - Server metadata, capabilities, and status
- `server://health` - Comprehensive health check of all components  
- `config://settings` - Safe configuration values

## 🎯 Prompt Templates

Built-in prompts for optimal AI assistant interaction:

- **System Prompt**: Comprehensive guidance for using all server capabilities
- **Error Handling Guide**: Troubleshooting and recovery strategies

## 🧪 Local Testing

The included CLI tool allows testing without Claude Desktop:

```bash
# Interactive mode
uv run python cli.py interactive

# Direct tool testing
uv run python cli.py calculate add 2 3
uv run python cli.py file read data/example.txt
uv run python cli.py search web "python tutorial"

# Health and diagnostics
uv run python cli.py health
uv run python cli.py demo

# Get help
uv run python cli.py --help
uv run python cli.py calculator --help
```

## 🔗 Claude Desktop Integration

1. **Start the MCP server**:
```bash
uv run python main.py
```

2. **Add to your Claude Desktop configuration**:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/mcp-template"
    }
  }
}
```

3. **Restart Claude Desktop** and test the connection

## 🤖 Claude Code Integration

**Claude Code** is Anthropic's official CLI for agentic coding workflows. This template is optimized for Claude Code usage:

### Setup for Claude Code

1. **Install Claude Code**: Follow the [official installation guide](https://docs.anthropic.com/en/docs/claude-code)

2. **Configure MCP Server**:

**Project Settings** (`.claude/settings.json`):
```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/mcp-template",
      "env": {
        "ENVIRONMENT": "development"
      }
    }
  },
  "rules": {
    "allowedTools": ["mcp__template.*"],
    "toolTimeout": 30000
  }
}
```

3. **Add Project Memory** (`CLAUDE.md`):
```markdown
# MCP Template Server

This project provides a template MCP server with:
- 🧮 Calculator: Mathematical operations with validation
- 📁 File Manager: Secure file operations in data/ directory  
- 🔍 Search: Web search with domain filtering (template)

Available tools: calculate, manage_file, search_web
Security: Sandboxed operations, input validation, path protection
```

4. **Test Integration**:
```bash
# In Claude Code terminal
uv run python cli.py health
uv run python cli.py demo
```

### Claude Code Workflow Integration

This template follows the **5-Step MCP Development Workflow** optimized for Claude Code:

1. **📚 Research & Documentation Scan**
   - Gather API docs and requirements
   - Update project memory (`CLAUDE.md`)

2. **🎯 Define Core MCP Functions**
   - Map functionality to MCP concepts (tools, resources, prompts)
   - Create Pydantic models for validation

3. **📝 Create Implementation Plan** 
   - Break down into testable components
   - Plan testing and security approach

4. **🔧 Build & Test Server/API**
   - Implement tools with CLI testing
   - Validate with `uv run python cli.py`

5. **🚀 Implement & Validate MCP**
   - Integrate with FastMCP server
   - Test in Claude Code environment

Each step includes git checkpoints for version control and rollback capabilities.

### Advanced Claude Code Features

**Memory Management:**
- Project context in `CLAUDE.md` 
- Import references with `@path/to/file`
- Automatic context loading

**Tool Permissions:**
```json
{
  "rules": {
    "allowedTools": ["mcp__template.*"],
    "disallowedTools": ["mcp__template__file_delete"],
    "toolTimeout": 30000
  }
}
```

**Development Workflow:**
```bash
# Claude Code optimized commands
uv run python cli.py health         # Check tool status
uv run python cli.py interactive    # Interactive testing
uv run pytest --cov=src            # Run tests
uv run ruff check --fix .          # Code quality
```

### Example Claude Desktop Config
```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/Users/username/projects/mcp-template",
      "env": {
        "ENVIRONMENT": "production"
      }
    }
  }
}
```

## 🏗️ Architecture

### Project Structure
```
mcp-template/
├── src/
│   ├── config.py           # 🎛️ Central configuration
│   ├── models.py           # 📊 Pydantic data models
│   ├── server.py           # 🚀 FastMCP server implementation
│   └── tools/              # 🔧 Tool implementations
│       ├── calculator.py   # 🧮 Mathematical operations
│       ├── file_manager.py # 📁 Secure file operations
│       └── search.py       # 🔍 Web search capabilities
├── tests/                  # 🧪 Comprehensive test suite
├── main.py                 # 🚀 Production entry point
├── cli.py                  # 🧪 Local testing CLI
└── pyproject.toml         # 📦 Project configuration
```

### Key Design Principles

- **Central Configuration**: All settings in `src/config.py`
- **Single Responsibility**: Each tool has one clear purpose
- **Early Returns**: Validate inputs first, handle errors gracefully
- **Type Safety**: Pydantic models for all data structures
- **Security First**: Sandboxed operations and input validation
- **Self-Documenting**: Clear names with minimal but helpful docstrings

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test categories
uv run pytest -m integration
uv run pytest -m performance
uv run pytest tests/test_models.py
```

**Test Coverage Goals:**
- 80%+ code coverage
- All error paths tested
- Edge cases validated
- Performance benchmarks

## 🔒 Security

This template implements multiple security layers:

- **Input Validation**: All inputs validated with Pydantic models
- **Path Sanitization**: Prevents directory traversal attacks
- **File System Sandboxing**: Operations restricted to safe directories
- **Resource Limits**: File sizes, request counts, and timeouts
- **Safe Defaults**: Secure fallbacks for all operations
- **No Sensitive Data Exposure**: Logs and responses are sanitized

## ⚙️ Configuration

Configuration is centralized in `src/config.py`. Key settings:

```python
# Application settings
APP_NAME = "MCP Template Server"
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# Performance settings
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
CACHE_SIZE = 1000

# Security settings
FILE_MANAGER_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_READ_PATHS = [str(DATA_DIR), str(ASSETS_DIR)]

# Feature flags
ENABLE_CACHE = True
ENABLE_LOGGING = True
ENABLE_METRICS = False
```

### Environment Variables

- `DEBUG=true` - Enable debug logging and verbose errors
- `ENVIRONMENT=production` - Set environment mode
- Custom variables can be added to `src/config.py`

## 🛠️ Development

This template includes a structured **5-Step Development Workflow** in `WORKFLOW.md`:

1. **📚 Research & Documentation Scan** - Gather requirements and API docs
2. **🎯 Define Core MCP Functions** - Map to tools, resources, prompts  
3. **📝 Create Implementation Plan** - Break down into testable components
4. **🔧 Build & Test Server/API** - Implement with CLI validation
5. **🚀 Implement & Validate MCP** - Full integration and testing

Each step includes git checkpoints for rollback capability.

### Adding New Tools

Follow the workflow in `WORKFLOW.md` or use this quick reference:

1. **Define data models** in `src/models.py`
2. **Implement tool class** in `src/tools/your_tool.py`
3. **Add server integration** in `src/server.py`
4. **Create tests** in `tests/test_tools.py`
5. **Update CLI** in `cli.py` for local testing

See `CLAUDE.md` for detailed development instructions and `src/tools/README.md` for implementation patterns.

### Code Quality

```bash
# Lint and format
uv run ruff check --fix .
uv run ruff format .

# Type checking
uv run mypy src/

# Security check
uv run bandit -r src/
```

### Adding Dependencies

```bash
# Runtime dependencies
uv add package-name

# Development dependencies  
uv add --dev package-name
```

## 🚨 Troubleshooting

### Common Issues

**ImportError when running commands**
```bash
# Solution: Use uv run for all commands
uv run python main.py
```

**File permission errors**
```bash
# Solution: Ensure data directory exists and is writable
mkdir -p data
chmod 755 data
```

**Tests failing**
```bash
# Solution: Install dev dependencies and run verbose
uv sync --dev
uv run pytest -v
```

**MCP server not connecting to Claude Desktop**
```bash
# Check server logs
DEBUG=true uv run python main.py

# Verify config path is absolute
# Restart Claude Desktop after config changes
```

### Getting Help

1. Check `CLAUDE.md` for detailed development instructions
2. Use `uv run python cli.py --help` for CLI usage
3. Review test files for usage examples
4. Check server logs with `DEBUG=true`

## 📈 Performance

The template is optimized for performance:

- **FastMCP**: High-performance MCP server framework
- **Async Support**: Non-blocking operations where beneficial
- **Caching**: Configurable caching for expensive operations
- **Resource Limits**: Prevents resource exhaustion
- **Efficient Validation**: Pydantic for fast data validation

Performance benchmarks (run with `uv run pytest -m performance`):
- Calculator: 1000+ operations/second
- File operations: 100+ files/second
- Search: Respects rate limits with caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the coding standards
4. Add tests for new functionality
5. Ensure all tests pass and coverage is maintained
6. Submit a pull request

### Development Setup

```bash
git clone https://github.com/yourusername/mcp-template.git
cd mcp-template
uv sync --dev
uv run pre-commit install  # If using pre-commit hooks
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) team
- [FastMCP](https://github.com/modelcontextprotocol/python-sdk) developers
- [UV](https://docs.astral.sh/uv/) for excellent package management
- [Pydantic](https://docs.pydantic.dev/) for data validation
- [Ruff](https://github.com/astral-sh/ruff) for code formatting

## 🔗 Related Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/download)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk#fastmcp)

---

**Happy building! 🚀** 

This template provides everything you need to create production-ready MCP servers. Start by exploring the example tools, then customize and extend them for your specific use case.