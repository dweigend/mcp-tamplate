"""🧪 MCP Template Tests Package.

Comprehensive test suite for the MCP Template Server.
Tests all tools, models, and server functionality.

Test Structure:
- test_models.py: Pydantic model validation tests
- test_tools.py: Individual tool functionality tests  
- test_server.py: Server integration and health tests

Test Coverage Goals:
- 80%+ code coverage
- All error paths tested
- Edge cases validated
- Performance benchmarks

References:
- pytest documentation
- Pydantic testing patterns
- MCP testing best practices
"""

import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_DATA_DIR.mkdir(exist_ok=True)

# Common test fixtures and utilities can be added here
__all__ = ["TEST_DATA_DIR"]