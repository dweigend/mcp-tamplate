"""🧪 Tests for MCP Server - Integration and Health Tests.

Tests for the main MCP server functionality, health checks,
and integration between components.

Test Coverage:
- Server initialization and configuration
- Health check endpoints
- Tool integration with server
- Error handling and logging
- Server resources and prompts

References:
- MCP Python SDK testing patterns
- FastMCP testing approaches
- pytest best practices
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock, patch

from src.server import (
    setup_logging,
    mcp,
    calculator_tool,
    file_manager_tool,
    search_tool,
)
from src.config import (
    APP_NAME,
    VERSION,
    SERVER_NAME,
    ENABLE_LOGGING,
)
from src.models import (
    CalculatorInput,
    FileManagerInput,
    SearchQuery,
    OperationType,
    FileOperation,
)


class TestServerInitialization:
    """🚀 Tests for server initialization and setup."""
    
    def test_logging_setup(self):
        """📊 Test logging configuration."""
        logger = setup_logging()
        
        assert logger.name == SERVER_NAME
        assert len(logger.handlers) > 0
        
        # Should have console handler
        console_handlers = [h for h in logger.handlers if hasattr(h, 'stream')]
        assert len(console_handlers) > 0
        
        # Should have file handler if logging enabled
        if ENABLE_LOGGING:
            file_handlers = [h for h in logger.handlers if hasattr(h, 'baseFilename')]
            assert len(file_handlers) > 0
    
    def test_server_instance(self):
        """🚀 Test MCP server instance."""
        assert mcp is not None
        assert hasattr(mcp, 'tool')
        assert hasattr(mcp, 'resource')
        assert hasattr(mcp, 'prompt')
    
    def test_tool_instances(self):
        """🔧 Test tool instances initialization."""
        assert calculator_tool is not None
        assert file_manager_tool is not None
        assert search_tool is not None
        
        # Test tool initialization
        calculator_tool.initialize()
        file_manager_tool.initialize()
        search_tool.initialize()
        
        assert calculator_tool._initialized
        assert file_manager_tool._initialized
        assert search_tool._initialized


class TestServerResources:
    """📚 Tests for server resource endpoints."""
    
    def test_server_info_resource(self):
        """⚙️ Test server info resource."""
        from src.server import get_server_info
        
        info = get_server_info()
        
        assert info.name == APP_NAME
        assert info.version == VERSION
        assert info.tools_count == 3  # calculator, file_manager, search
        assert info.uptime >= 0
        assert info.status == "running"
        assert len(info.capabilities) > 0
        
        expected_capabilities = [
            "mathematical_calculations",
            "file_operations",
            "web_search",
            "health_monitoring"
        ]
        for capability in expected_capabilities:
            assert capability in info.capabilities
    
    def test_health_check_resource(self):
        """💚 Test health check resource."""
        from src.server import get_health_status
        
        health = get_health_status()
        
        assert health.status in ["healthy", "degraded"]
        assert health.response_time >= 0
        assert isinstance(health.checks, dict)
        
        # Expected health checks
        expected_checks = [
            "server_running",
            "tools_available",
            "file_system_accessible",
            "calculator_functional",
            "search_available",
            "logging_working"
        ]
        
        for check in expected_checks:
            assert check in health.checks
            assert isinstance(health.checks[check], bool)
    
    def test_configuration_resource(self):
        """⚙️ Test configuration resource."""
        from src.server import get_configuration
        
        config = get_configuration()
        
        assert isinstance(config, dict)
        assert "server" in config
        assert "limits" in config
        assert "search" in config
        assert "features" in config
        
        # Server configuration
        assert config["server"]["name"] == SERVER_NAME
        assert config["server"]["version"] == VERSION
        
        # Should not expose sensitive information
        assert "api_key" not in str(config).lower()
        assert "password" not in str(config).lower()
        assert "secret" not in str(config).lower()


class TestServerPrompts:
    """🎯 Tests for server prompt templates."""
    
    def test_system_prompt(self):
        """🎯 Test system prompt generation."""
        from src.server import system_prompt
        
        prompt = system_prompt()
        
        assert isinstance(prompt, str)
        assert len(prompt) > 100  # Should be substantial
        assert APP_NAME in prompt
        assert VERSION in prompt
        
        # Should mention available tools
        assert "Calculator" in prompt
        assert "File Manager" in prompt
        assert "Search" in prompt
        
        # Should mention security features
        assert "Security" in prompt or "security" in prompt
        assert "sandbox" in prompt.lower()
    
    def test_error_handling_guide(self):
        """🚨 Test error handling guide prompt."""
        from src.server import error_handling_guide
        
        guide = error_handling_guide()
        
        assert isinstance(guide, str)
        assert len(guide) > 200  # Should be comprehensive
        
        # Should cover different error types
        assert "Calculator" in guide
        assert "File" in guide
        assert "Search" in guide
        
        # Should provide troubleshooting steps
        assert "Troubleshooting" in guide
        assert "Error Response Format" in guide


class TestServerToolIntegration:
    """🔗 Tests for tool integration with server wrapper functions."""
    
    def test_calculate_tool_integration(self):
        """🧮 Test calculator tool integration."""
        from src.server import calculate
        
        calc_input = CalculatorInput(
            operation=OperationType.ADD,
            numbers=[2.0, 3.0],
            precision=2
        )
        
        response = calculate(calc_input)
        
        assert response.success is True
        assert response.data is not None
        assert response.error is None
        assert response.execution_time >= 0
        
        # Check calculation result
        result = response.data
        assert result.result == 5.0
        assert result.formatted_result == "5.00"
    
    def test_calculate_tool_error_handling(self):
        """🧮 Test calculator tool error handling."""
        from src.server import calculate
        
        # Test division by zero
        calc_input = CalculatorInput(
            operation=OperationType.DIVIDE,
            numbers=[10.0, 0.0]
        )
        
        response = calculate(calc_input)
        
        assert response.success is False
        assert response.data is None
        assert response.error is not None
        assert response.error.code == "CALCULATION_ERROR"
        assert "divide by zero" in response.error.message.lower()
    
    def test_file_manager_tool_integration(self):
        """📁 Test file manager tool integration."""
        from src.server import manage_file
        
        # Test file existence check
        file_input = FileManagerInput(
            operation=FileOperation.EXISTS,
            path="nonexistent_file.txt"
        )
        
        response = manage_file(file_input)
        
        assert response.success is True
        assert response.data is not None
        assert response.error is None
        
        # Check file manager result
        result = response.data
        assert result.operation == FileOperation.EXISTS
        assert "does not exist" in result.message.lower()
    
    def test_file_manager_tool_error_handling(self):
        """📁 Test file manager tool error handling."""
        from src.server import manage_file
        
        # Test path traversal attempt
        file_input = FileManagerInput(
            operation=FileOperation.READ,
            path="../../../etc/passwd"
        )
        
        response = manage_file(file_input)
        
        assert response.success is False
        assert response.error is not None
        assert response.error.code == "FILE_OPERATION_ERROR"
    
    def test_search_tool_integration(self):
        """🔍 Test search tool integration."""
        from src.server import search_web
        
        search_query = SearchQuery(
            text="python tutorial",
            limit=2
        )
        
        response = search_web(search_query)
        
        assert response.success is True
        assert response.data is not None
        assert response.error is None
        
        # Check search result
        result = response.data
        assert result.query == "python tutorial"
        assert len(result.results) <= 2
    
    def test_search_tool_error_handling(self):
        """🔍 Test search tool error handling."""
        from src.server import search_web
        
        # Test empty query
        search_query = SearchQuery(
            text="",  # Empty query should cause validation error
            limit=5
        )
        
        with pytest.raises(Exception):  # Should fail validation
            search_web(search_query)


class TestServerErrorHandling:
    """🚨 Tests for server-level error handling."""
    
    @patch('src.server.calculator_tool')
    def test_tool_failure_handling(self, mock_calculator):
        """🚨 Test handling of tool failures."""
        from src.server import calculate
        
        # Mock tool to raise exception
        mock_calculator.calculate.side_effect = Exception("Tool failure")
        
        calc_input = CalculatorInput(
            operation=OperationType.ADD,
            numbers=[1.0, 2.0]
        )
        
        response = calculate(calc_input)
        
        assert response.success is False
        assert response.error is not None
        assert response.error.code == "CALCULATION_ERROR"
        assert "Tool failure" in response.error.message
    
    def test_invalid_input_handling(self):
        """🚨 Test handling of invalid inputs."""
        from src.server import calculate
        
        # This should be caught by Pydantic validation before reaching the tool
        with pytest.raises(Exception):  # ValidationError or similar
            calculate("invalid input")


class TestServerConfiguration:
    """⚙️ Tests for server configuration validation."""
    
    def test_config_validation(self):
        """⚙️ Test configuration validation."""
        from src.config import validate_config
        
        # Should not raise exception with valid config
        validate_config()
    
    def test_environment_detection(self):
        """🌍 Test environment detection."""
        from src.config import get_environment, is_development, is_production
        
        env = get_environment()
        assert env in ["development", "staging", "production"]
        
        # Test boolean helpers
        is_dev = is_development()
        is_prod = is_production()
        
        assert isinstance(is_dev, bool)
        assert isinstance(is_prod, bool)
        
        # Can't be both dev and prod
        assert not (is_dev and is_prod)


class TestServerPerformance:
    """⚡ Performance tests for server operations."""
    
    def test_health_check_performance(self):
        """⚡ Test health check response time."""
        from src.server import get_health_status
        import time
        
        start_time = time.time()
        health = get_health_status()
        elapsed_time = time.time() - start_time
        
        # Health check should be fast
        assert elapsed_time < 1.0
        assert health.response_time < 1.0
    
    def test_server_info_performance(self):
        """⚡ Test server info response time."""
        from src.server import get_server_info
        import time
        
        start_time = time.time()
        info = get_server_info()
        elapsed_time = time.time() - start_time
        
        # Server info should be instant
        assert elapsed_time < 0.1
        assert info.uptime >= 0


@pytest.mark.integration
class TestServerIntegration:
    """🔗 Integration tests for complete server workflows."""
    
    def test_complete_calculation_workflow(self):
        """🔗 Test complete calculation workflow."""
        from src.server import calculate, get_health_status
        
        # Check health first
        health = get_health_status()
        assert health.status in ["healthy", "degraded"]
        
        # Perform calculation
        calc_input = CalculatorInput(
            operation=OperationType.MULTIPLY,
            numbers=[3.0, 4.0],
            precision=1
        )
        
        response = calculate(calc_input)
        
        assert response.success is True
        assert response.data.result == 12.0
        assert response.data.formatted_result == "12.0"
    
    def test_complete_file_workflow(self):
        """🔗 Test complete file management workflow."""
        from src.server import manage_file
        
        filename = "integration_test.txt"
        content = "Integration test content"
        
        # Write file
        write_input = FileManagerInput(
            operation=FileOperation.WRITE,
            path=filename,
            content=content
        )
        
        write_response = manage_file(write_input)
        assert write_response.success is True
        
        # Read file
        read_input = FileManagerInput(
            operation=FileOperation.READ,
            path=filename
        )
        
        read_response = manage_file(read_input)
        assert read_response.success is True
        assert content in read_response.data.content
        
        # Delete file
        delete_input = FileManagerInput(
            operation=FileOperation.DELETE,
            path=filename
        )
        
        delete_response = manage_file(delete_input)
        assert delete_response.success is True
    
    def test_error_recovery_workflow(self):
        """🔗 Test error recovery and graceful degradation."""
        from src.server import calculate, get_health_status
        
        # Cause an error
        calc_input = CalculatorInput(
            operation=OperationType.DIVIDE,
            numbers=[1.0, 0.0]
        )
        
        error_response = calculate(calc_input)
        assert error_response.success is False
        
        # Server should still be healthy after error
        health = get_health_status()
        assert health.status in ["healthy", "degraded"]
        
        # Should be able to perform successful operation after error
        calc_input = CalculatorInput(
            operation=OperationType.ADD,
            numbers=[1.0, 2.0]
        )
        
        success_response = calculate(calc_input)
        assert success_response.success is True