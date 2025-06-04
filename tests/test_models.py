"""🧪 Tests for Pydantic Models - Data Validation and Serialization.

Comprehensive tests for all Pydantic models used in the MCP server.
Validates input sanitization, error handling, and data integrity.

Test Coverage:
- Valid input validation
- Invalid input rejection
- Edge cases and boundary conditions
- Serialization/deserialization
- Custom validators

References:
- Pydantic testing documentation
- pytest best practices
"""

from __future__ import annotations

import pytest
from datetime import datetime
from typing import List

from pydantic import ValidationError

from src.models import (
    CalculatorInput,
    CalculatorResult,
    FileManagerInput,
    FileManagerResult,
    SearchQuery,
    SearchResult,
    SearchResponse,
    ErrorDetail,
    ToolResponse,
    ServerInfo,
    HealthCheck,
    OperationType,
    FileOperation,
    LogLevel,
)


class TestCalculatorModels:
    """🧮 Tests for calculator-related models."""
    
    def test_calculator_input_valid(self):
        """✅ Test valid calculator input."""
        calc_input = CalculatorInput(
            operation=OperationType.ADD,
            numbers=[1.0, 2.0, 3.0],
            precision=2
        )
        
        assert calc_input.operation == OperationType.ADD
        assert calc_input.numbers == [1.0, 2.0, 3.0]
        assert calc_input.precision == 2
    
    def test_calculator_input_default_precision(self):
        """✅ Test default precision value."""
        calc_input = CalculatorInput(
            operation=OperationType.MULTIPLY,
            numbers=[2.0, 3.0]
        )
        
        assert calc_input.precision == 2  # Default value
    
    def test_calculator_input_invalid_operation(self):
        """❌ Test invalid operation type."""
        with pytest.raises(ValidationError) as exc_info:
            CalculatorInput(
                operation="invalid_operation",
                numbers=[1.0, 2.0]
            )
        
        assert "operation" in str(exc_info.value)
    
    def test_calculator_input_empty_numbers(self):
        """❌ Test empty numbers list."""
        with pytest.raises(ValidationError) as exc_info:
            CalculatorInput(
                operation=OperationType.ADD,
                numbers=[]
            )
        
        assert "min_items" in str(exc_info.value)
    
    def test_calculator_input_too_many_numbers(self):
        """❌ Test too many numbers (> 10)."""
        with pytest.raises(ValidationError) as exc_info:
            CalculatorInput(
                operation=OperationType.ADD,
                numbers=list(range(11))  # 11 numbers
            )
        
        assert "max_items" in str(exc_info.value)
    
    def test_calculator_input_invalid_precision(self):
        """❌ Test invalid precision values."""
        # Negative precision
        with pytest.raises(ValidationError):
            CalculatorInput(
                operation=OperationType.ADD,
                numbers=[1.0, 2.0],
                precision=-1
            )
        
        # Too high precision
        with pytest.raises(ValidationError):
            CalculatorInput(
                operation=OperationType.ADD,
                numbers=[1.0, 2.0],
                precision=16
            )
    
    def test_calculator_input_division_by_zero_validation(self):
        """❌ Test division by zero validation."""
        with pytest.raises(ValidationError) as exc_info:
            CalculatorInput(
                operation=OperationType.DIVIDE,
                numbers=[10.0, 0.0]
            )
        
        assert "divide by zero" in str(exc_info.value).lower()
    
    def test_calculator_input_binary_operation_validation(self):
        """❌ Test binary operations require exactly 2 numbers."""
        binary_operations = [
            OperationType.SUBTRACT,
            OperationType.DIVIDE,
            OperationType.POWER,
            OperationType.MODULO
        ]
        
        for operation in binary_operations:
            # Too few numbers
            with pytest.raises(ValidationError):
                CalculatorInput(
                    operation=operation,
                    numbers=[5.0]
                )
            
            # Too many numbers
            with pytest.raises(ValidationError):
                CalculatorInput(
                    operation=operation,
                    numbers=[1.0, 2.0, 3.0]
                )
    
    def test_calculator_result_valid(self):
        """✅ Test valid calculator result."""
        result = CalculatorResult(
            result=5.0,
            operation=OperationType.ADD,
            input_numbers=[2.0, 3.0],
            formatted_result="5.00"
        )
        
        assert result.result == 5.0
        assert result.operation == OperationType.ADD
        assert result.input_numbers == [2.0, 3.0]
        assert result.formatted_result == "5.00"
        assert isinstance(result.calculation_time, datetime)


class TestFileManagerModels:
    """📁 Tests for file manager models."""
    
    def test_file_manager_input_valid(self):
        """✅ Test valid file manager input."""
        file_input = FileManagerInput(
            operation=FileOperation.READ,
            path="data/test.txt",
            encoding="utf-8"
        )
        
        assert file_input.operation == FileOperation.READ
        assert file_input.path == "data/test.txt"
        assert file_input.encoding == "utf-8"
    
    def test_file_manager_input_write_operation(self):
        """✅ Test write operation with content."""
        file_input = FileManagerInput(
            operation=FileOperation.WRITE,
            path="data/output.txt",
            content="Hello, World!"
        )
        
        assert file_input.operation == FileOperation.WRITE
        assert file_input.content == "Hello, World!"
    
    def test_file_manager_input_invalid_path(self):
        """❌ Test invalid path values."""
        # Empty path
        with pytest.raises(ValidationError):
            FileManagerInput(
                operation=FileOperation.READ,
                path=""
            )
        
        # Path too long
        with pytest.raises(ValidationError):
            FileManagerInput(
                operation=FileOperation.READ,
                path="x" * 501  # Exceeds 500 char limit
            )
    
    def test_file_manager_input_path_traversal_validation(self):
        """❌ Test path traversal protection."""
        dangerous_paths = [
            "../../../etc/passwd",
            "data/../../../secrets.txt",
            "/absolute/path/file.txt"
        ]
        
        for dangerous_path in dangerous_paths:
            with pytest.raises(ValidationError) as exc_info:
                FileManagerInput(
                    operation=FileOperation.READ,
                    path=dangerous_path
                )
            
            assert "traversal" in str(exc_info.value).lower() or "absolute" in str(exc_info.value).lower()
    
    def test_file_manager_input_write_requires_content(self):
        """❌ Test write operation requires content."""
        with pytest.raises(ValidationError) as exc_info:
            FileManagerInput(
                operation=FileOperation.WRITE,
                path="data/test.txt"
                # Missing content
            )
        
        assert "content required" in str(exc_info.value).lower()
    
    def test_file_manager_input_content_size_limit(self):
        """❌ Test content size limits."""
        large_content = "x" * (1_000_001)  # Exceeds 1MB limit
        
        with pytest.raises(ValidationError):
            FileManagerInput(
                operation=FileOperation.WRITE,
                path="data/large.txt",
                content=large_content
            )


class TestSearchModels:
    """🔍 Tests for search-related models."""
    
    def test_search_query_valid(self):
        """✅ Test valid search query."""
        query = SearchQuery(
            text="python tutorial",
            domains=["docs.python.org", "realpython.com"],
            limit=5,
            language="en"
        )
        
        assert query.text == "python tutorial"
        assert query.domains == ["docs.python.org", "realpython.com"]
        assert query.limit == 5
        assert query.language == "en"
    
    def test_search_query_defaults(self):
        """✅ Test default values."""
        query = SearchQuery(text="test query")
        
        assert query.domains == []
        assert query.limit == 10
        assert query.language == "en"
    
    def test_search_query_invalid_text(self):
        """❌ Test invalid search text."""
        # Empty text
        with pytest.raises(ValidationError):
            SearchQuery(text="")
        
        # Text too long
        with pytest.raises(ValidationError):
            SearchQuery(text="x" * 1001)
    
    def test_search_query_invalid_limit(self):
        """❌ Test invalid limit values."""
        # Limit too low
        with pytest.raises(ValidationError):
            SearchQuery(text="test", limit=0)
        
        # Limit too high
        with pytest.raises(ValidationError):
            SearchQuery(text="test", limit=101)
    
    def test_search_query_too_many_domains(self):
        """❌ Test too many domain filters."""
        too_many_domains = [f"domain{i}.com" for i in range(11)]
        
        with pytest.raises(ValidationError):
            SearchQuery(
                text="test",
                domains=too_many_domains
            )
    
    def test_search_query_invalid_domains(self):
        """❌ Test invalid domain formats."""
        invalid_domains = [
            "invalid_domain",  # No TLD
            "",  # Empty
            "space domain.com"  # Contains space
        ]
        
        for invalid_domain in invalid_domains:
            with pytest.raises(ValidationError):
                SearchQuery(
                    text="test",
                    domains=[invalid_domain]
                )
    
    def test_search_query_domain_normalization(self):
        """✅ Test domain normalization to lowercase."""
        query = SearchQuery(
            text="test",
            domains=["EXAMPLE.COM", "GitHub.com"]
        )
        
        assert query.domains == ["example.com", "github.com"]
    
    def test_search_result_valid(self):
        """✅ Test valid search result."""
        result = SearchResult(
            title="Test Title",
            url="https://example.com/page",
            snippet="This is a test snippet",
            domain="example.com",
            relevance_score=0.85
        )
        
        assert result.title == "Test Title"
        assert result.url == "https://example.com/page"
        assert result.snippet == "This is a test snippet"
        assert result.domain == "example.com"
        assert result.relevance_score == 0.85
    
    def test_search_result_optional_relevance(self):
        """✅ Test search result without relevance score."""
        result = SearchResult(
            title="Test Title",
            url="https://example.com/page",
            snippet="Test snippet",
            domain="example.com"
        )
        
        assert result.relevance_score is None
    
    def test_search_result_invalid_relevance_score(self):
        """❌ Test invalid relevance scores."""
        # Score too low
        with pytest.raises(ValidationError):
            SearchResult(
                title="Test",
                url="https://example.com",
                snippet="Test",
                domain="example.com",
                relevance_score=-0.1
            )
        
        # Score too high
        with pytest.raises(ValidationError):
            SearchResult(
                title="Test",
                url="https://example.com",
                snippet="Test",
                domain="example.com",
                relevance_score=1.1
            )
    
    def test_search_response_valid(self):
        """✅ Test valid search response."""
        results = [
            SearchResult(
                title="Result 1",
                url="https://example1.com",
                snippet="Snippet 1",
                domain="example1.com"
            ),
            SearchResult(
                title="Result 2",
                url="https://example2.com",
                snippet="Snippet 2",
                domain="example2.com"
            )
        ]
        
        response = SearchResponse(
            query="test query",
            results=results,
            total_found=2,
            search_time=0.123
        )
        
        assert response.query == "test query"
        assert len(response.results) == 2
        assert response.total_found == 2
        assert response.search_time == 0.123
        assert isinstance(response.timestamp, datetime)


class TestErrorModels:
    """🚨 Tests for error handling models."""
    
    def test_error_detail_valid(self):
        """✅ Test valid error detail."""
        error = ErrorDetail(
            code="TEST_ERROR",
            message="This is a test error",
            details={"param": "value"},
            traceback="Traceback info"
        )
        
        assert error.code == "TEST_ERROR"
        assert error.message == "This is a test error"
        assert error.details == {"param": "value"}
        assert error.traceback == "Traceback info"
        assert isinstance(error.timestamp, datetime)
    
    def test_error_detail_minimal(self):
        """✅ Test minimal error detail."""
        error = ErrorDetail(
            code="SIMPLE_ERROR",
            message="Simple error message"
        )
        
        assert error.code == "SIMPLE_ERROR"
        assert error.message == "Simple error message"
        assert error.details is None
        assert error.traceback is None
    
    def test_tool_response_success(self):
        """✅ Test successful tool response."""
        response = ToolResponse(
            success=True,
            data={"result": "success"},
            execution_time=0.456
        )
        
        assert response.success is True
        assert response.data == {"result": "success"}
        assert response.error is None
        assert response.execution_time == 0.456
        assert isinstance(response.timestamp, datetime)
    
    def test_tool_response_error(self):
        """✅ Test error tool response."""
        error = ErrorDetail(
            code="TOOL_ERROR",
            message="Tool failed"
        )
        
        response = ToolResponse(
            success=False,
            error=error,
            execution_time=0.123
        )
        
        assert response.success is False
        assert response.data is None
        assert response.error == error
        assert response.execution_time == 0.123
    
    def test_tool_response_negative_execution_time(self):
        """❌ Test negative execution time validation."""
        with pytest.raises(ValidationError):
            ToolResponse(
                success=True,
                execution_time=-0.1
            )


class TestServerModels:
    """⚙️ Tests for server-related models."""
    
    def test_server_info_valid(self):
        """✅ Test valid server info."""
        info = ServerInfo(
            name="Test Server",
            version="1.0.0",
            description="Test description",
            capabilities=["calc", "file", "search"],
            tools_count=3,
            uptime=123.45
        )
        
        assert info.name == "Test Server"
        assert info.version == "1.0.0"
        assert info.description == "Test description"
        assert info.capabilities == ["calc", "file", "search"]
        assert info.tools_count == 3
        assert info.uptime == 123.45
        assert info.status == "running"  # Default value
    
    def test_server_info_invalid_tools_count(self):
        """❌ Test negative tools count."""
        with pytest.raises(ValidationError):
            ServerInfo(
                name="Test",
                version="1.0.0",
                description="Test",
                capabilities=[],
                tools_count=-1,  # Invalid
                uptime=0.0
            )
    
    def test_health_check_valid(self):
        """✅ Test valid health check."""
        health = HealthCheck(
            status="healthy",
            checks={
                "database": True,
                "cache": False,
                "external_api": True
            },
            response_time=0.025
        )
        
        assert health.status == "healthy"
        assert health.checks["database"] is True
        assert health.checks["cache"] is False
        assert health.response_time == 0.025
        assert isinstance(health.timestamp, datetime)
    
    def test_health_check_defaults(self):
        """✅ Test health check default values."""
        health = HealthCheck(response_time=0.1)
        
        assert health.status == "healthy"
        assert health.checks == {}
        assert isinstance(health.timestamp, datetime)
    
    def test_health_check_negative_response_time(self):
        """❌ Test negative response time validation."""
        with pytest.raises(ValidationError):
            HealthCheck(response_time=-0.1)


class TestEnumValidation:
    """🔢 Tests for enum validation."""
    
    def test_operation_type_values(self):
        """✅ Test all operation type enum values."""
        expected_operations = ["add", "subtract", "multiply", "divide", "power", "modulo"]
        
        for op in expected_operations:
            operation = OperationType(op)
            assert operation.value == op
    
    def test_file_operation_values(self):
        """✅ Test all file operation enum values."""
        expected_operations = ["read", "write", "list", "exists", "delete"]
        
        for op in expected_operations:
            operation = FileOperation(op)
            assert operation.value == op
    
    def test_log_level_values(self):
        """✅ Test all log level enum values."""
        expected_levels = ["debug", "info", "warning", "error", "critical"]
        
        for level in expected_levels:
            log_level = LogLevel(level)
            assert log_level.value == level


@pytest.mark.parametrize("operation,numbers,should_pass", [
    (OperationType.ADD, [1.0, 2.0, 3.0], True),
    (OperationType.SUBTRACT, [5.0, 3.0], True),
    (OperationType.MULTIPLY, [2.0, 3.0, 4.0], True),
    (OperationType.DIVIDE, [10.0, 2.0], True),
    (OperationType.POWER, [2.0, 3.0], True),
    (OperationType.MODULO, [10.0, 3.0], True),
    (OperationType.DIVIDE, [10.0, 0.0], False),  # Division by zero
    (OperationType.SUBTRACT, [5.0], False),  # Too few numbers
    (OperationType.POWER, [2.0, 3.0, 4.0], False),  # Too many numbers
])
def test_calculator_input_parametrized(operation, numbers, should_pass):
    """🧮 Parametrized tests for calculator input validation."""
    if should_pass:
        calc_input = CalculatorInput(
            operation=operation,
            numbers=numbers
        )
        assert calc_input.operation == operation
        assert calc_input.numbers == numbers
    else:
        with pytest.raises(ValidationError):
            CalculatorInput(
                operation=operation,
                numbers=numbers
            )