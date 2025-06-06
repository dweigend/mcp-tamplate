# 📋 Configuration Examples

Example configurations for MCP server integration.

## Files

- `claude_desktop_config.json` - Claude Desktop configuration
- `claude_code_config.json` - Claude Code configuration  

## Usage

### Claude Desktop (macOS)
```bash
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Claude Code (Project)
```bash
mkdir -p .claude
cp claude_code_config.json .claude/settings.json
```

## Configuration Format

```json
{
  "mcpServers": {
    "your-server": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/server"
    }
  }
}
```

📖 **See MCP Documentation**: https://modelcontextprotocol.io/docs/tools/claude-desktop