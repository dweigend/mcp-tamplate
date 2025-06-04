# 🧪 Tests Directory

Comprehensive test suite ensuring reliability and correctness of the MCP Template Server.

## 📋 Overview

The test suite follows pytest best practices with:
- **80%+ code coverage** target
- **Fast execution** with parallel test support
- **Clear test organization** by component
- **Comprehensive scenarios** including edge cases
- **Mock external dependencies** for reliable testing

## 📁 Test Structure

```
tests/
├── __init__.py           # Test package setup
├── test_models.py        # Pydantic model validation tests
├── test_tools.py         # Individual tool functionality tests
├── test_server.py        # Server integration tests
└── data/                 # Test data and fixtures
    └── test_files/       # Sample files for testing
```

## 🧪 Test Categories

### 📊 Model Tests (`test_models.py`)

Tests for Pydantic data validation and serialization:

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

Tests for individual tool implementations:

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

Tests for MCP server integration and health:

```python
class TestServerIntegration:
    def test_tool_integration(self):
        # Test server wrapper functions
        
    def test_resource_endpoints(self):
        # Test server info, health, config
        
    def test_error_recovery(self):
        # Test graceful error handling
```

**Coverage:**
- Server initialization 🚀
- Tool integration 🔗
- Resource endpoints 📚
- Health monitoring 💚
- Error recovery 🚨
- Configuration validation ⚙️

## 🎯 Test Execution

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py -v

# Run specific test class
uv run pytest tests/test_tools.py::TestCalculatorTool -v

# Run with performance markers
uv run pytest -m performance

# Run integration tests only
uv run pytest -m integration
```

### Test Markers

```python
@pytest.mark.integration
def test_complete_workflow():
    # Integration test
    pass

@pytest.mark.performance
def test_calculation_speed():
    # Performance benchmark
    pass

@pytest.mark.security
def test_path_traversal_protection():
    # Security validation
    pass
```

### Coverage Targets

- **Overall Coverage:** 80%+ required
- **Critical Paths:** 95%+ (security, validation)
- **Tool Logic:** 90%+ (core functionality)
- **Error Handling:** 85%+ (exception paths)

## 🔧 Test Fixtures

### Common Fixtures

```python
@pytest.fixture
def temp_data_dir():
    """Temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def sample_calculator_input():
    """Valid calculator input for testing."""
    return CalculatorInput(
        operation=OperationType.ADD,
        numbers=[2.0, 3.0],
        precision=2
    )

@pytest.fixture
def mock_search_results():
    """Mock search API responses."""
    return [
        {"title": "Test Result", "url": "https://example.com"},
        # ... more results
    ]
```

### Tool-Specific Fixtures

```python
class TestFileManagerTool:
    @pytest.fixture
    def temp_file(self):
        """Create temporary test file."""
        test_file = TEST_DATA_DIR / "temp_test.txt"
        test_file.write_text("Test content")
        yield test_file
        if test_file.exists():
            test_file.unlink()
```

## 🚨 Error Testing Strategy

### Exception Path Coverage

```python
def test_division_by_zero(self, calculator):
    """Test division by zero handling."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calculator.calculate(OperationType.DIVIDE, [10.0, 0.0])

def test_file_not_found(self, file_manager):
    """Test file not found handling."""
    result = file_manager.execute_operation(
        FileOperation.READ, 
        "nonexistent.txt"
    )
    assert result.success is False
    assert "not found" in result.message.lower()
```

### Input Validation Testing

```python
@pytest.mark.parametrize("operation,numbers,should_pass", [
    (OperationType.ADD, [1.0, 2.0], True),
    (OperationType.DIVIDE, [10.0, 0.0], False),  # Division by zero
    (OperationType.SUBTRACT, [5.0], False),      # Too few numbers
])
def test_calculator_input_validation(operation, numbers, should_pass):
    """Parametrized input validation tests."""
    if should_pass:
        calc_input = CalculatorInput(operation=operation, numbers=numbers)
        assert calc_input.operation == operation
    else:
        with pytest.raises(ValidationError):
            CalculatorInput(operation=operation, numbers=numbers)
```

## 🔒 Security Testing

### Path Traversal Tests

```python
def test_path_traversal_prevention(self, file_manager):
    """Test path traversal attack prevention."""
    dangerous_paths = [
        "../../../etc/passwd",
        "/absolute/path/secrets.txt",
        "data/../../../config.json"
    ]
    
    for path in dangerous_paths:
        result = file_manager.execute_operation(FileOperation.READ, path)
        assert result.success is False
        assert "traversal" in result.message.lower() or "denied" in result.message.lower()
```

### Input Sanitization Tests

```python
def test_malicious_input_handling(self, search_tool):
    """Test malicious input sanitization."""
    malicious_queries = [
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "../../etc/passwd",
    ]
    
    for query in malicious_queries:
        with pytest.raises(ValidationError):
            SearchQuery(text=query)
```

## ⚡ Performance Testing

### Benchmark Tests

```python
@pytest.mark.performance
def test_calculator_performance(self):
    """Test calculator performance with multiple operations."""
    calc = CalculatorTool()
    calc.initialize()
    
    start_time = time.time()
    for i in range(1000):
        calc.calculate(OperationType.ADD, [i, i+1])
    elapsed = time.time() - start_time
    
    assert elapsed < 1.0, f"Calculator too slow: {elapsed}s for 1000 operations"

@pytest.mark.performance  
def test_file_operations_performance(self):
    """Test file operations performance."""
    fm = FileManagerTool()
    fm.initialize()
    
    # Test multiple file operations
    start_time = time.time()
    for i in range(100):
        content = f"Test content {i}"
        filename = f"perf_test_{i}.txt"
        
        fm.execute_operation(FileOperation.WRITE, filename, content=content)
        fm.execute_operation(FileOperation.READ, filename)
        fm.execute_operation(FileOperation.DELETE, filename)
    
    elapsed = time.time() - start_time
    assert elapsed < 5.0, f"File operations too slow: {elapsed}s for 300 operations"
```

## 🔗 Integration Testing

### End-to-End Workflows

```python
@pytest.mark.integration
def test_complete_calculation_workflow(self):
    """Test complete calculation workflow through server."""
    # Test server wrapper integration
    calc_input = CalculatorInput(
        operation=OperationType.MULTIPLY,
        numbers=[3.0, 4.0],
        precision=1
    )
    
    response = calculate(calc_input)  # Server function
    
    assert response.success is True
    assert response.data.result == 12.0
    assert response.execution_time > 0

@pytest.mark.integration
def test_error_recovery_workflow(self):
    """Test server error recovery."""
    # Cause an error
    calc_input = CalculatorInput(
        operation=OperationType.DIVIDE,
        numbers=[1.0, 0.0]
    )
    
    error_response = calculate(calc_input)
    assert error_response.success is False
    
    # Server should recover for next operation
    calc_input = CalculatorInput(
        operation=OperationType.ADD,
        numbers=[1.0, 2.0]
    )
    
    success_response = calculate(calc_input)
    assert success_response.success is True
```

## 📊 Test Configuration

### pytest.ini Settings

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-fail-under=80",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "performance: marks tests as performance benchmarks",
    "security: marks tests as security validation",
]
```

### Mock Configuration

```python
# Mock external dependencies
@patch('src.tools.search.requests.get')
def test_search_api_integration(self, mock_get):
    """Test search with mocked API."""
    mock_get.return_value.json.return_value = {
        "results": [{"title": "Test", "url": "https://example.com"}]
    }
    
    search_tool = SearchTool()
    results = search_tool.search("test query")
    
    assert len(results.results) > 0
    mock_get.assert_called_once()
```

## 🚀 Best Practices

### Test Organization
- **One test class per component**
- **Descriptive test names** that explain what is tested
- **Clear assertions** with helpful error messages
- **Isolated tests** that don't depend on each other

### Test Data Management
- **Use fixtures** for common test data
- **Clean up** temporary files and resources
- **Mock external dependencies** for reliability
- **Parameterize** similar test cases

### Debugging Tests
```bash
# Run specific failing test with verbose output
uv run pytest tests/test_tools.py::TestCalculatorTool::test_division_by_zero -vvs

# Run with debugger on failure
uv run pytest --pdb tests/test_models.py

# Generate detailed coverage report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```