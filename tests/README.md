# 🧪 Tests

Example test suite for the MCP template server.

## Test Files

- `test_models.py` - Pydantic model validation tests
- `test_tools.py` - Tool functionality tests
- `test_server.py` - Server integration tests

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html

# Specific file
uv run pytest tests/test_tools.py -v
```

## Test Pattern

```python
class TestComponent:
    @pytest.fixture
    def component(self):
        """Setup test component."""
        return Component()
    
    def test_success_case(self, component):
        """Test normal operation."""
        assert component.execute() == expected
    
    def test_error_case(self, component):
        """Test error handling."""
        with pytest.raises(ValueError):
            component.execute(invalid_input)
```

## Coverage Target

Minimum 80% code coverage required.