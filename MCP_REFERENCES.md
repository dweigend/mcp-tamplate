# 🔗 MCP Architecture Reference

## Core Components

### 1. **Tools** 🔧
- **Purpose**: Executable functionality exposed to LLMs
- **Pattern**: Model-controlled with human approval
- **Structure**: Name, description, input schema, optional annotations
- **Examples**: System operations, API integrations, data processing

### 2. **Resources** 📁
- **Purpose**: Static/dynamic data exposure to LLMs
- **Pattern**: Application-controlled access
- **Types**: Text (UTF-8) or Binary (base64) content
- **Examples**: Files, database records, live system data

### 3. **Prompts** 💬
- **Purpose**: Reusable LLM interaction templates
- **Pattern**: User-controlled selection and execution
- **Structure**: Name, description, optional arguments
- **Examples**: Code explanations, commit messages, workflows

### 4. **Sampling** 🎯
- **Purpose**: Server requests LLM completions via client
- **Pattern**: Human-in-the-loop design
- **Use Cases**: Agentic workflows, context-based decisions
- **Control**: User maintains approval authority

### 5. **Transports** 🚀
- **Stdio**: Local process communication
- **HTTP/SSE**: Remote server communication
- **Protocol**: JSON-RPC 2.0 wire format

## Architecture Principles

### Separation of Concerns
```
Client ↔ Transport ↔ Server
                   ├── Tools (executable)
                   ├── Resources (data)
                   ├── Prompts (templates)
                   └── Sampling (LLM requests)
```

### Security First
- Validate all inputs
- Sanitize data
- Implement access controls
- Use secure transports (TLS)
- Rate limiting

### Clean Code Patterns
- **Single Responsibility**: Each component has one clear purpose
- **Early Returns**: Validate inputs first
- **Type Safety**: Use schemas for all data
- **Error Handling**: Graceful failure patterns

## Future Features (Roadmap)

### Agents Integration
- **Agent Graphs**: Complex topologies with namespacing
- **Interactive Workflows**: Enhanced human-in-the-loop
- **Google ADK Compatibility**: For agent frameworks

### Infrastructure
- **MCP Registry**: Centralized discovery
- **Reference Clients**: Standard implementations
- **Compliance Tests**: Automated verification

## Template Architecture

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

### Key Principles
1. **API Layer**: Separate external connections from MCP logic
2. **Examples**: All tools/resources/prompts are demonstrations
3. **Modularity**: Clean separation between components
4. **Testability**: Each component independently testable
5. **Extensibility**: Easy to add new functionality