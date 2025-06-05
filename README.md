# 🔧 MCP Template
This is an early version and is currently under active development. I am making constant changes.
A simple, clean template for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers with Python and FastMCP.

> **This is a template with example implementations.** All tools, resources, and prompts are demonstrations showing how to structure MCP components.

## ✨ What's Included

- 🔧 **Example Tools**: Calculator, file manager, search (demonstration patterns)
- 📁 **Example Resources**: Server info and configuration access
- 💬 **Example Prompts**: System guidance templates
- 🧪 **Testing Framework**: CLI tool for local development
- 🔒 **Security Patterns**: Input validation and safe operations
- 📖 **Clean Architecture**: Separation of API, tools, and MCP logic

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <this-repo>
cd mcp-template
uv sync

# 2. Test locally
uv run python cli.py demo

# 3. Start MCP server
uv run python main.py
```

## 📋 Example Tools

> These are **demonstration tools** showing MCP patterns. Replace with your own implementations.

### 🧮 Calculator
```bash
uv run python cli.py calculator add 2 3
```

### 📁 File Manager
```bash
uv run python cli.py file read data/test.txt
```

### 🔍 Search (Mock)
```bash
uv run python cli.py search web "tutorial"
```

## 🔗 Claude Desktop Integration

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

Add to: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows)

## 🏗️ Architecture

```
src/
├── server.py           # 🚀 MCP server (FastMCP)
├── api/               # 🌐 External API connections
├── tools/             # 🔧 Tool implementations (examples)
├── resources/         # 📁 Resource handlers (examples)
├── prompts/           # 💬 Prompt templates (examples)
├── models.py          # 📊 Pydantic schemas
└── config.py          # ⚙️ Configuration
```

### Design Principles
- **API Separation**: External connections isolated from MCP logic
- **Examples**: All tools/resources/prompts are demonstrations
- **Clean Architecture**: Single responsibility, type safety, early returns

## 🛠️ Development

```bash
# Test everything
uv run pytest

# Code quality
uv run ruff check --fix .

# Add dependencies
uv add package-name
```

See `CLAUDE.md` and `MCP_REFERENCES.md` for detailed development guidance.

---

**This is a template** - replace example tools with your own implementations! 🚀
