# 📋 Configuration Examples

> These are example configurations for integrating the MCP template with Claude Desktop and Claude Code.

## 🔗 Claude Desktop

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

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

## 🤖 Claude Code

**File:** `.claude/settings.json` (project)

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

See the included example configuration files:
- `claude_desktop_config.json` - Claude Desktop setup
- `claude_code_config.json` - Claude Code setup

