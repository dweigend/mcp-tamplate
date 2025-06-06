# 💬 MCP Prompts

Reusable prompt templates for enhanced LLM interactions.

## What are MCP Prompts?

User-controlled templates that guide LLM behavior.

📖 **See MCP Documentation**: https://modelcontextprotocol.io/docs/concepts/prompts

## Current Files

- `system_guide.py` - Server capabilities and usage examples
- `error_handling.py` - Troubleshooting guide for common errors

## Pattern

```python
def get_prompt_name() -> str:
    """Return formatted prompt template."""
    return f"""
    Prompt content with {dynamic_values}
    """
```