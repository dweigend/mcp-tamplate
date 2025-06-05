# 🧪 Example Tests

> This directory contains example tests demonstrating testing patterns for MCP servers.

## 📋 Overview

Example test patterns showing:
- Component testing (tools, resources, prompts)
- API layer mocking  
- Security validation
- Performance benchmarks
- Integration testing

## 📁 Test Structure

```
tests/
├── test_models.py        # Example model validation tests
├── test_tools.py         # Example tool functionality tests  
├── test_server.py        # Example server integration tests
```

## 🧪 Test Categories

### 📊 Model Tests (`test_models.py`)

Example tests for Pydantic data validation:

```python
class TestCalculatorModels:
    def test_valid_input(self):
        # Test successful model creation
        
    def test_invalid_input(self):
        # Test validation error handling
        
    def test_edge_cases(self):
        # Test boundary conditions
```

**Coverage:**
- Valid input validation ✅
- Invalid input rejection ❌
- Edge cases and boundaries 🔄
- Serialization/deserialization 📤📥
- Custom validator logic ✅

### 🔧 Tool Tests (`test_tools.py`)

Example tests for tool implementations:

```python
class TestCalculatorTool:
    @pytest.fixture
    def calculator(self):
        calc = CalculatorTool()
        calc.initialize()
        return calc
    
    def test_basic_operations(self, calculator):
        # Test each mathematical operation
        
    def test_error_handling(self, calculator):
        # Test division by zero, invalid inputs
        
    def test_precision_formatting(self, calculator):
        # Test decimal precision handling
```

**Coverage:**
- Tool initialization 🔧
- Health checks 💚
- Valid operations ✅
- Error conditions ❌
- Security validation 🔒
- Performance benchmarks ⚡

### 🚀 Server Tests (`test_server.py`)

Example tests for MCP server integration:

```python
class TestServerIntegration:
    def test_tool_integration(self):
        # Test server wrapper functions
        
    def test_resource_endpoints(self):
        # Test server info, health, config
        
    def test_error_recovery(self):
        # Test graceful error handling
```

## 🎯 Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py -v
```

These examples demonstrate testing patterns for MCP servers. Customize for your specific implementations.