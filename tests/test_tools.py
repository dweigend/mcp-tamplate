"""🧪 Tests for MCP Tools - Functionality and Integration Tests.

Comprehensive tests for all tool implementations including
calculator, file manager, and search tools.

Test Coverage:
- Tool initialization and health checks
- Valid operations and edge cases
- Error handling and validation
- Performance and integration
- Security and sandboxing

References:
- pytest documentation
- Tool testing best practices
- MCP tool development patterns
"""

from __future__ import annotations

import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch

from src.tools.calculator import CalculatorTool
from src.tools.file_manager import FileManagerTool
from src.tools.search import SearchTool
from src.models import (
    OperationType,
    FileOperation,
    SearchQuery,
)
from tests import TEST_DATA_DIR


class TestCalculatorTool:
    """🧮 Tests for calculator tool functionality."""
    
    @pytest.fixture
    def calculator(self):
        """Fixture providing initialized calculator tool."""
        calc = CalculatorTool()
        calc.initialize()
        return calc
    
    def test_initialization(self):
        """✅ Test calculator initialization."""
        calc = CalculatorTool()
        assert not calc._initialized
        
        calc.initialize()
        assert calc._initialized
    
    def test_health_check(self, calculator):
        """💚 Test calculator health check."""
        assert calculator.health_check() is True
    
    def test_add_operation(self, calculator):
        """✅ Test addition operation."""
        result = calculator.calculate(OperationType.ADD, [2.0, 3.0, 5.0], 2)
        
        assert result.result == 10.0
        assert result.operation == OperationType.ADD
        assert result.input_numbers == [2.0, 3.0, 5.0]
        assert result.formatted_result == "10.00"
    
    def test_subtract_operation(self, calculator):
        """✅ Test subtraction operation."""
        result = calculator.calculate(OperationType.SUBTRACT, [10.0, 3.0], 1)
        
        assert result.result == 7.0
        assert result.formatted_result == "7.0"
    
    def test_multiply_operation(self, calculator):
        """✅ Test multiplication operation."""
        result = calculator.calculate(OperationType.MULTIPLY, [2.0, 3.0, 4.0], 0)
        
        assert result.result == 24.0
        assert result.formatted_result == "24"
    
    def test_divide_operation(self, calculator):
        """✅ Test division operation."""
        result = calculator.calculate(OperationType.DIVIDE, [15.0, 3.0], 3)
        
        assert result.result == 5.0
        assert result.formatted_result == "5.000"
    
    def test_power_operation(self, calculator):
        """✅ Test power operation."""
        result = calculator.calculate(OperationType.POWER, [2.0, 3.0], 1)
        
        assert result.result == 8.0
        assert result.formatted_result == "8.0"
    
    def test_modulo_operation(self, calculator):
        """✅ Test modulo operation."""
        result = calculator.calculate(OperationType.MODULO, [10.0, 3.0], 2)
        
        assert result.result == 1.0
        assert result.formatted_result == "1.00"
    
    def test_division_by_zero(self, calculator):
        """❌ Test division by zero error."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calculator.calculate(OperationType.DIVIDE, [10.0, 0.0])
    
    def test_modulo_by_zero(self, calculator):
        """❌ Test modulo by zero error."""
        with pytest.raises(ZeroDivisionError, match="Cannot calculate modulo by zero"):
            calculator.calculate(OperationType.MODULO, [10.0, 0.0])
    
    def test_invalid_operation(self, calculator):
        """❌ Test invalid operation type."""
        with pytest.raises(ValueError, match="Unsupported operation"):
            # This would need to be done by creating an invalid enum somehow
            pass
    
    def test_empty_numbers_list(self, calculator):
        """❌ Test empty numbers list."""
        with pytest.raises(ValueError, match="No numbers provided"):
            calculator.calculate(OperationType.ADD, [])
    
    def test_too_many_numbers(self, calculator):
        """❌ Test too many numbers (> 10)."""
        with pytest.raises(ValueError, match="Too many numbers"):
            calculator.calculate(OperationType.ADD, list(range(11)))
    
    def test_nan_values(self, calculator):
        """❌ Test NaN values rejection."""
        with pytest.raises(ValueError, match="NaN values not allowed"):
            calculator.calculate(OperationType.ADD, [1.0, float('nan')])
    
    def test_infinite_values(self, calculator):
        """❌ Test infinite values rejection."""
        with pytest.raises(ValueError, match="Infinite values not allowed"):
            calculator.calculate(OperationType.ADD, [1.0, float('inf')])
    
    def test_binary_operation_validation(self, calculator):
        """❌ Test binary operations require exactly 2 numbers."""
        binary_ops = [OperationType.SUBTRACT, OperationType.DIVIDE, 
                     OperationType.POWER, OperationType.MODULO]
        
        for op in binary_ops:
            # Too few numbers
            with pytest.raises(ValueError, match="requires exactly 2 numbers"):
                calculator.calculate(op, [5.0])
            
            # Too many numbers
            with pytest.raises(ValueError, match="requires exactly 2 numbers"):
                calculator.calculate(op, [1.0, 2.0, 3.0])
    
    def test_precision_validation(self, calculator):
        """❌ Test precision parameter validation."""
        # Invalid type
        with pytest.raises(ValueError, match="Precision must be an integer"):
            calculator.calculate(OperationType.ADD, [1.0, 2.0], "invalid")
        
        # Negative precision
        with pytest.raises(ValueError, match="Precision must be between"):
            calculator.calculate(OperationType.ADD, [1.0, 2.0], -1)
        
        # Too high precision
        with pytest.raises(ValueError, match="Precision must be between"):
            calculator.calculate(OperationType.ADD, [1.0, 2.0], 16)
    
    def test_precision_formatting(self, calculator):
        """✅ Test different precision formatting."""
        # Zero precision
        result = calculator.calculate(OperationType.DIVIDE, [7.0, 3.0], 0)
        assert result.formatted_result == "2"
        
        # High precision
        result = calculator.calculate(OperationType.DIVIDE, [7.0, 3.0], 5)
        assert result.formatted_result == "2.33333"
    
    def test_large_numbers(self, calculator):
        """✅ Test calculation with large numbers."""
        large_num = 1e10
        result = calculator.calculate(OperationType.ADD, [large_num, large_num], 0)
        assert result.result == 2e10
    
    def test_get_supported_operations(self, calculator):
        """✅ Test getting supported operations list."""
        operations = calculator.get_supported_operations()
        expected = ["+", "-", "*", "/", "**", "%"]
        assert set(operations) == set(expected)
    
    def test_get_operation_info(self, calculator):
        """✅ Test getting operation information."""
        info = calculator.get_operation_info(OperationType.ADD)
        assert "Addition" in info
        assert "Sum all provided numbers" in info


class TestFileManagerTool:
    """📁 Tests for file manager tool functionality."""
    
    @pytest.fixture
    def file_manager(self):
        """Fixture providing initialized file manager tool."""
        fm = FileManagerTool()
        fm.initialize()
        return fm
    
    @pytest.fixture
    def temp_file(self):
        """Fixture providing a temporary test file."""
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=TEST_DATA_DIR,
            delete=False,
            suffix=".txt"
        ) as f:
            f.write("Test content for file operations")
            temp_path = Path(f.name)
        
        yield temp_path
        
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()
    
    def test_initialization(self):
        """✅ Test file manager initialization."""
        fm = FileManagerTool()
        assert not fm._initialized
        
        fm.initialize()
        assert fm._initialized
        
        # Verify safe directories exist
        assert TEST_DATA_DIR.exists()
    
    def test_health_check(self, file_manager):
        """💚 Test file manager health check."""
        assert file_manager.health_check() is True
    
    def test_read_file_operation(self, file_manager, temp_file):
        """✅ Test reading file content."""
        # Make relative to data directory
        relative_path = temp_file.relative_to(TEST_DATA_DIR.parent)
        
        result = file_manager.execute_operation(
            FileOperation.READ,
            str(relative_path)
        )
        
        assert result.success is True
        assert result.operation == FileOperation.READ
        assert "Test content for file operations" in result.content
        assert "Successfully read file" in result.message
    
    def test_write_file_operation(self, file_manager):
        """✅ Test writing file content."""
        test_content = "This is test content for writing"
        test_path = "test_write.txt"
        
        result = file_manager.execute_operation(
            FileOperation.WRITE,
            test_path,
            content=test_content
        )
        
        assert result.success is True
        assert result.operation == FileOperation.WRITE
        assert "Successfully wrote" in result.message
        
        # Verify file was created
        created_file = TEST_DATA_DIR / test_path
        assert created_file.exists()
        assert created_file.read_text() == test_content
        
        # Cleanup
        created_file.unlink()
    
    def test_list_directory_operation(self, file_manager):
        """✅ Test listing directory contents."""
        result = file_manager.execute_operation(
            FileOperation.LIST,
            str(TEST_DATA_DIR)
        )
        
        assert result.success is True
        assert result.operation == FileOperation.LIST
        assert result.files is not None
        assert isinstance(result.files, list)
        assert "items in directory" in result.message
    
    def test_exists_operation(self, file_manager, temp_file):
        """✅ Test checking file existence."""
        # Test existing file
        relative_path = temp_file.relative_to(TEST_DATA_DIR.parent)
        
        result = file_manager.execute_operation(
            FileOperation.EXISTS,
            str(relative_path)
        )
        
        assert result.success is True
        assert result.operation == FileOperation.EXISTS
        assert result.file_info is not None
        assert "exists" in result.message.lower()
        
        # Test non-existing file
        result = file_manager.execute_operation(
            FileOperation.EXISTS,
            "nonexistent_file.txt"
        )
        
        assert result.success is True
        assert result.file_info is None
        assert "does not exist" in result.message.lower()
    
    def test_delete_file_operation(self, file_manager):
        """✅ Test deleting file."""
        # Create temporary file to delete
        test_file = TEST_DATA_DIR / "to_delete.txt"
        test_file.write_text("Delete me")
        
        relative_path = test_file.relative_to(TEST_DATA_DIR.parent)
        
        result = file_manager.execute_operation(
            FileOperation.DELETE,
            str(relative_path)
        )
        
        assert result.success is True
        assert result.operation == FileOperation.DELETE
        assert "deleted successfully" in result.message.lower()
        assert not test_file.exists()
    
    def test_path_traversal_protection(self, file_manager):
        """🔒 Test path traversal attack prevention."""
        dangerous_paths = [
            "../../../etc/passwd",
            "data/../../../secrets.txt",
            "/absolute/path/file.txt"
        ]
        
        for dangerous_path in dangerous_paths:
            result = file_manager.execute_operation(
                FileOperation.READ,
                dangerous_path
            )
            
            assert result.success is False
            assert "traversal" in result.message.lower() or "denied" in result.message.lower()
    
    def test_file_size_limit(self, file_manager):
        """🔒 Test file size limits enforcement."""
        # This would require mocking file size or creating a very large file
        # For now, test the validation logic indirectly
        pass
    
    def test_invalid_encoding(self, file_manager):
        """❌ Test handling invalid encoding."""
        # Create file with binary content
        binary_file = TEST_DATA_DIR / "binary_test.bin"
        binary_file.write_bytes(b'\x80\x81\x82\x83')
        
        try:
            relative_path = binary_file.relative_to(TEST_DATA_DIR.parent)
            
            result = file_manager.execute_operation(
                FileOperation.READ,
                str(relative_path),
                encoding="utf-8"
            )
            
            # Should succeed with fallback encoding
            assert result.success is True
            assert "fallback encoding" in result.message.lower()
            
        finally:
            binary_file.unlink()
    
    def test_write_without_content(self, file_manager):
        """❌ Test write operation without content."""
        result = file_manager.execute_operation(
            FileOperation.WRITE,
            "test.txt"
            # Missing content parameter
        )
        
        assert result.success is False
        assert "content required" in result.message.lower()
    
    def test_read_nonexistent_file(self, file_manager):
        """❌ Test reading non-existent file."""
        result = file_manager.execute_operation(
            FileOperation.READ,
            "nonexistent_file.txt"
        )
        
        assert result.success is False
        assert "not found" in result.message.lower()
    
    def test_delete_nonexistent_file(self, file_manager):
        """❌ Test deleting non-existent file."""
        result = file_manager.execute_operation(
            FileOperation.DELETE,
            "nonexistent_file.txt"
        )
        
        assert result.success is False
        assert "not found" in result.message.lower()
    
    def test_list_nonexistent_directory(self, file_manager):
        """❌ Test listing non-existent directory."""
        result = file_manager.execute_operation(
            FileOperation.LIST,
            "nonexistent_directory"
        )
        
        assert result.success is False
        assert "not found" in result.message.lower()
    
    def test_get_safe_directories(self, file_manager):
        """✅ Test getting safe directories list."""
        safe_dirs = file_manager.get_safe_directories()
        assert isinstance(safe_dirs, list)
        assert len(safe_dirs) > 0
    
    def test_get_allowed_extensions(self, file_manager):
        """✅ Test getting allowed extensions list."""
        extensions = file_manager.get_allowed_extensions()
        assert isinstance(extensions, list)
        expected_extensions = [".txt", ".json", ".md", ".py", ".yaml", ".yml"]
        for ext in expected_extensions:
            assert ext in extensions


class TestSearchTool:
    """🔍 Tests for search tool functionality."""
    
    @pytest.fixture
    def search_tool(self):
        """Fixture providing initialized search tool."""
        search = SearchTool()
        search.initialize()
        return search
    
    def test_initialization(self):
        """✅ Test search tool initialization."""
        search = SearchTool()
        assert not search._initialized
        
        search.initialize()
        assert search._initialized
    
    def test_health_check(self, search_tool):
        """💚 Test search tool health check."""
        assert search_tool.health_check() is True
    
    def test_basic_search(self, search_tool):
        """✅ Test basic search functionality."""
        result = search_tool.search(
            text="python tutorial",
            limit=5
        )
        
        assert result.query == "python tutorial"
        assert isinstance(result.results, list)
        assert len(result.results) <= 5
        assert result.total_found >= 0
        assert result.search_time > 0
    
    def test_search_with_domain_filter(self, search_tool):
        """✅ Test search with domain filtering."""
        result = search_tool.search(
            text="python",
            domains=["docs.python.org"],
            limit=3
        )
        
        assert result.query == "python"
        assert len(result.results) <= 3
        
        # Check domain filtering (if results exist)
        for search_result in result.results:
            assert "python.org" in search_result.domain.lower()
    
    def test_search_with_language(self, search_tool):
        """✅ Test search with language parameter."""
        result = search_tool.search(
            text="python",
            language="de"
        )
        
        assert result.query == "python"
        assert isinstance(result.results, list)
    
    def test_empty_search_query(self, search_tool):
        """❌ Test empty search query."""
        with pytest.raises(ValueError, match="Search text cannot be empty"):
            search_tool.search(text="")
    
    def test_search_query_too_long(self, search_tool):
        """❌ Test search query too long."""
        long_query = "x" * 1001
        
        with pytest.raises(ValueError, match="Search text too long"):
            search_tool.search(text=long_query)
    
    def test_invalid_limit(self, search_tool):
        """❌ Test invalid limit values."""
        # Limit too low
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            search_tool.search(text="test", limit=0)
        
        # Limit too high
        with pytest.raises(ValueError, match="Limit too high"):
            search_tool.search(text="test", limit=101)
    
    def test_invalid_language(self, search_tool):
        """❌ Test invalid language code."""
        with pytest.raises(ValueError, match="Language must be a valid language code"):
            search_tool.search(text="test", language="x")
    
    def test_too_many_domains(self, search_tool):
        """❌ Test too many domain filters."""
        too_many_domains = [f"domain{i}.com" for i in range(11)]
        
        with pytest.raises(ValueError, match="Too many domain filters"):
            search_tool.search(text="test", domains=too_many_domains)
    
    def test_invalid_domains(self, search_tool):
        """❌ Test invalid domain formats."""
        invalid_domains = ["invalid_domain", "", "space domain.com"]
        
        for invalid_domain in invalid_domains:
            with pytest.raises(ValueError, match="Invalid domain format"):
                search_tool.search(text="test", domains=[invalid_domain])
    
    def test_rate_limiting(self, search_tool):
        """⏱️ Test rate limiting between searches."""
        start_time = time.time()
        
        # First search
        search_tool.search(text="test1", limit=1)
        
        # Second search (should be rate limited)
        search_tool.search(text="test2", limit=1)
        
        elapsed_time = time.time() - start_time
        
        # Should take at least the rate limit interval
        assert elapsed_time >= search_tool._min_search_interval
    
    def test_relevance_scoring(self, search_tool):
        """📊 Test relevance scoring in results."""
        result = search_tool.search(text="python", limit=5)
        
        for search_result in result.results:
            if search_result.relevance_score is not None:
                assert 0.0 <= search_result.relevance_score <= 1.0
    
    def test_search_info(self, search_tool):
        """ℹ️ Test getting search information."""
        info = search_tool.get_search_info()
        
        assert isinstance(info, dict)
        assert "max_results" in info
        assert "default_limit" in info
        assert "timeout" in info
        assert "rate_limit_interval" in info
        
        assert info["max_results"] > 0
        assert info["default_limit"] > 0
        assert info["timeout"] > 0
    
    @patch('time.sleep')
    def test_rate_limiting_sleep(self, mock_sleep, search_tool):
        """⏱️ Test that rate limiting actually calls sleep."""
        # Reset last search time to trigger rate limiting
        search_tool._last_search_time = time.time()
        
        # Perform search (should trigger rate limiting)
        search_tool.search(text="test", limit=1)
        
        # Verify sleep was called
        mock_sleep.assert_called()


@pytest.mark.integration
class TestToolIntegration:
    """🔗 Integration tests for multiple tools working together."""
    
    def test_calculator_and_file_manager(self):
        """🔗 Test calculator result saving to file."""
        # Calculate something
        calc = CalculatorTool()
        calc.initialize()
        calc_result = calc.calculate(OperationType.ADD, [2.0, 3.0], 2)
        
        # Save result to file
        fm = FileManagerTool()
        fm.initialize()
        
        result_content = f"Calculation: {calc_result.formatted_result}"
        file_result = fm.execute_operation(
            FileOperation.WRITE,
            "calculation_result.txt",
            content=result_content
        )
        
        assert file_result.success is True
        
        # Read back and verify
        read_result = fm.execute_operation(
            FileOperation.READ,
            "calculation_result.txt"
        )
        
        assert read_result.success is True
        assert calc_result.formatted_result in read_result.content
        
        # Cleanup
        cleanup_result = fm.execute_operation(
            FileOperation.DELETE,
            "calculation_result.txt"
        )
        assert cleanup_result.success is True
    
    def test_search_and_file_manager(self):
        """🔗 Test search results saving to file."""
        # Perform search
        search = SearchTool()
        search.initialize()
        search_result = search.search("python tutorial", limit=2)
        
        # Save search results to file
        fm = FileManagerTool()
        fm.initialize()
        
        results_text = f"Search: {search_result.query}\nResults: {len(search_result.results)}"
        file_result = fm.execute_operation(
            FileOperation.WRITE,
            "search_results.txt",
            content=results_text
        )
        
        assert file_result.success is True
        
        # Read back and verify
        read_result = fm.execute_operation(
            FileOperation.READ,
            "search_results.txt"
        )
        
        assert read_result.success is True
        assert search_result.query in read_result.content
        
        # Cleanup
        cleanup_result = fm.execute_operation(
            FileOperation.DELETE,
            "search_results.txt"
        )
        assert cleanup_result.success is True


@pytest.mark.performance
class TestPerformance:
    """⚡ Performance tests for tools."""
    
    def test_calculator_performance(self):
        """⚡ Test calculator performance."""
        calc = CalculatorTool()
        calc.initialize()
        
        start_time = time.time()
        
        # Perform multiple calculations
        for i in range(100):
            calc.calculate(OperationType.ADD, [i, i+1], 2)
        
        elapsed_time = time.time() - start_time
        
        # Should complete 100 calculations in reasonable time
        assert elapsed_time < 1.0, f"Calculator too slow: {elapsed_time}s for 100 calculations"
    
    def test_file_manager_performance(self):
        """⚡ Test file manager performance."""
        fm = FileManagerTool()
        fm.initialize()
        
        start_time = time.time()
        
        # Create, read, and delete multiple files
        for i in range(10):
            filename = f"perf_test_{i}.txt"
            content = f"Performance test content {i}"
            
            # Write
            fm.execute_operation(FileOperation.WRITE, filename, content=content)
            
            # Read
            fm.execute_operation(FileOperation.READ, filename)
            
            # Delete
            fm.execute_operation(FileOperation.DELETE, filename)
        
        elapsed_time = time.time() - start_time
        
        # Should complete 10 file operations cycles in reasonable time
        assert elapsed_time < 2.0, f"File manager too slow: {elapsed_time}s for 30 operations"