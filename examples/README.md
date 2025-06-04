# 📋 Examples Directory

Configuration examples and integration templates for the MCP Template Server.

## 📁 Contents

```
examples/
├── README.md                      # This file
├── claude_desktop_config.json     # Claude Desktop integration
├── claude_code_config.json        # Claude Code integration  
├── settings_examples/             # Various configuration examples
│   ├── development.json           # Development environment
│   ├── production.json            # Production environment
│   └── custom_tools.json          # Custom tool configurations
└── workflows/                     # Workflow examples
    ├── basic_usage.md             # Basic MCP usage patterns
    ├── advanced_integration.md    # Advanced integration examples
    └── troubleshooting.md         # Common issues and solutions
```

## 🔗 Claude Desktop Integration

### Basic Configuration

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

### Production Configuration

```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/mcp-template",
      "env": {
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Configuration Locations

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

## 🤖 Claude Code Integration

### Settings Configuration

**File:** `.claude/settings.json` (project) or `~/.claude/settings.json` (global)

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
    "disallowedTools": [],
    "toolTimeout": 30000
  }
}
```

### Memory Integration

**File:** `CLAUDE.md` (project memory)

```markdown
# MCP Template Server Context

This project uses a custom MCP server for:
- Mathematical calculations with validation
- Secure file operations within data/ directory
- Web search capabilities (mock implementation)

## Available Tools
- `calculate`: Mathematical operations (add, subtract, multiply, divide, power, modulo)
- `manage_file`: File operations (read, write, list, exists, delete)
- `search_web`: Web search with domain filtering

## Security Notes
- File operations are sandboxed to data/ and assets/ directories
- All inputs are validated with Pydantic models
- Path traversal attacks are prevented

## Usage Patterns
1. Use calculate for mathematical operations
2. Use manage_file for data processing workflows
3. Use search_web for research tasks (template implementation)
```

### Environment Variables

```bash
# Development
export DEBUG=true
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG

# Production  
export DEBUG=false
export ENVIRONMENT=production
export LOG_LEVEL=INFO
```

## ⚙️ Configuration Examples

### Development Environment

```json
{
  "mcpServers": {
    "mcp-template-dev": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/mcp-template",
      "env": {
        "DEBUG": "true",
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "DEBUG"
      }
    }
  },
  "rules": {
    "allowedTools": ["mcp__template.*"],
    "toolTimeout": 60000
  }
}
```

### Production Environment

```json
{
  "mcpServers": {
    "mcp-template-prod": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/mcp-template",
      "env": {
        "DEBUG": "false", 
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "INFO"
      }
    }
  },
  "rules": {
    "allowedTools": ["mcp__template.*"],
    "disallowedTools": ["mcp__template__file_delete"],
    "toolTimeout": 30000
  }
}
```

### Custom Tool Configuration

```json
{
  "mcpServers": {
    "mcp-template": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/mcp-template",
      "env": {
        "CALCULATOR_MAX_PRECISION": "10",
        "SEARCH_DEFAULT_LIMIT": "5",
        "FILE_MANAGER_MAX_SIZE": "5242880"
      }
    }
  }
}
```

## 🔧 Usage Examples

### Basic Calculator Usage

```python
# In Claude Code or Claude Desktop
# Calculate compound interest
calculate(operation="power", numbers=[1.05, 10], precision=4)
# Result: 1.6289

# Calculate average
calculate(operation="add", numbers=[85, 92, 78, 95, 88], precision=1)
# Result: 87.6 (then divide by 5)
```

### File Operations

```python
# Create a data analysis file
manage_file(
    operation="write",
    path="data/analysis_results.txt", 
    content="Analysis Results\n================\nTotal: 1,234\nAverage: 87.6"
)

# Read configuration
manage_file(operation="read", path="data/config_example.json")

# List data directory
manage_file(operation="list", path="data/")
```

### Search Operations

```python
# Search for documentation
search_web(
    text="python pydantic validation tutorial",
    domains=["docs.pydantic.dev", "realpython.com"],
    limit=5
)

# Technical research
search_web(
    text="model context protocol MCP integration", 
    limit=10
)
```

## 🚨 Troubleshooting

### Common Issues

**1. Server Not Starting**
```bash
# Check logs
tail -f logs/mcp-server.log

# Test manually
uv run python main.py

# Validate configuration
uv run python cli.py health
```

**2. Permission Errors**
```bash
# Ensure directories exist and are writable
mkdir -p data logs
chmod 755 data logs

# Check file permissions
ls -la data/
```

**3. Tool Timeouts**
```json
{
  "rules": {
    "toolTimeout": 60000  // Increase timeout to 60 seconds
  }
}
```

**4. Path Issues**
- Always use **absolute paths** in configuration
- Ensure the `cwd` directory exists
- Check that UV is in the system PATH

### Validation Commands

```bash
# Test server health
uv run python cli.py health

# Test all tools
uv run python cli.py demo

# Check configuration
uv run python -c "from src.config import validate_config; validate_config()"

# Test specific tool
uv run python cli.py calculator calculate add 2 3
```

## 🔄 Integration Workflows

### 1. Development Setup

1. Clone and setup project
2. Configure Claude Code settings
3. Add project memory (`CLAUDE.md`)
4. Test with local CLI
5. Validate in Claude Code

### 2. Production Deployment

1. Set production environment variables
2. Update configuration with production settings
3. Test server startup
4. Configure monitoring and logging
5. Deploy with proper security settings

### 3. Custom Tool Development

1. Follow the 5-step workflow in `WORKFLOW.md`
2. Implement and test tools locally
3. Add to server integration
4. Update Claude Code configuration
5. Test end-to-end functionality

## 📚 Additional Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [FastMCP Framework](https://github.com/modelcontextprotocol/python-sdk)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🎯 Quick Start Checklist

- [ ] 📁 Set absolute path in configuration
- [ ] 🔧 Test with `uv run python cli.py health`
- [ ] ⚙️ Add configuration to Claude Desktop/Code
- [ ] 🔄 Restart Claude application
- [ ] ✅ Test tool usage in conversation
- [ ] 📊 Check logs for any issues
- [ ] 🚀 Start building with your MCP server!