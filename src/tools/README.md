# 🔧 Example Tools

> **These are demonstration tools** showing MCP implementation patterns. Replace with your own implementations.

## 📋 Overview

Example tools demonstrate how to structure MCP components:
- Input validation with Pydantic models  
- Security patterns and error handling
- Testing and CLI integration
- Clean architecture principles

## 🧮 Calculator Tool (`calculator.py`)

**Purpose:** Example tool demonstrating mathematical operations with validation.

**Features:**
- Support for 6 operations: add, subtract, multiply, divide, power, modulo
- Configurable decimal precision (0-15 places)
- Division by zero protection
- Input validation for operation-specific requirements
- High-precision decimal arithmetic

**Usage:**
```python
from src.tools.calculator import CalculatorTool
from src.models import OperationType

calc = CalculatorTool()
calc.initialize()

result = calc.calculate(
    operation=OperationType.ADD,
    numbers=[2.5, 3.7, 1.8],
    precision=2
)
print(result.formatted_result)  # "8.00"
```

**Security:**
- Validates number count for each operation type
- Prevents NaN and infinite value processing
- Limits input list to 10 numbers maximum
- Handles overflow conditions gracefully

## 📁 File Manager Tool (`file_manager.py`)

**Purpose:** Example tool demonstrating secure file operations within sandboxed directories.

**Features:**
- Read, write, list, delete, and existence check operations
- Path traversal attack prevention
- File size limit enforcement (10MB default)
- Encoding support with fallback handling
- Sandboxed to specific directories only

**Usage:**
```python
from src.tools.file_manager import FileManagerTool
from src.models import FileOperation

fm = FileManagerTool()
fm.initialize()

# Write a file
result = fm.execute_operation(
    operation=FileOperation.WRITE,
    path="data/example.txt",
    content="Hello, World!"
)

# Read it back
result = fm.execute_operation(
    operation=FileOperation.READ,
    path="data/example.txt"
)
print(result.content)  # "Hello, World!"
```

**Security:**
- Prevents path traversal with ".." detection
- Blocks absolute path access
- Restricts operations to allowed directories
- Validates file extensions against blocklist
- Enforces file size limits

## 🔍 Search Tool (`search.py`)

**Purpose:** Example tool demonstrating web search patterns (mock implementation for template).

**Features:**
- Mock search results for template purposes
- Domain filtering capabilities
- Configurable result limits (1-100)
- Language support
- Rate limiting protection
- Relevance scoring

**Usage:**
```python
from src.tools.search import SearchTool

search = SearchTool()
search.initialize()

results = search.search(
    text="python tutorial",
    domains=["docs.python.org"],
    limit=5
)

for result in results.results:
    print(f"{result.title}: {result.url}")
```

**Integration Points:**
```python
# Replace mock implementation with real API
def _integrate_google_search(self, query: str, **kwargs) -> List[dict]:
    # Google Custom Search API integration
    pass

def _integrate_bing_search(self, query: str, **kwargs) -> List[dict]:
    # Bing Search API integration
    pass
```

**Security:**
- Rate limiting between requests
- Domain validation
- Query length limits
- Input sanitization

## 🏗️ Tool Architecture

### Base Pattern

Every tool follows this pattern:

```python
class YourTool:
    def __init__(self) -> None:
        self._initialized = False
        # Setup instance variables
    
    def initialize(self) -> None:
        """Initialize tool with required setup."""
        if self._initialized:
            return
        # Initialization logic here
        self._initialized = True
        logger.info("🔧 Your tool initialized")
    
    def health_check(self) -> bool:
        """Verify tool is working correctly."""
        try:
            # Test basic functionality
            return True
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False
    
    def execute_operation(self, input_data) -> YourResult:
        """Main tool functionality with validation."""
        if not self._initialized:
            self.initialize()
        
        # Early return validation
        if not self._validate_input(input_data):
            return self._create_error_response("Invalid input")
        
        try:
            # Main processing logic
            result = self._process_data(input_data)
            return self._create_success_response(result)
        except Exception as e:
            logger.error(f"❌ Operation failed: {e}")
            return self._create_error_response(str(e))
```

### Integration with Server

Tools integrate with the MCP server through wrapper functions:

```python
@mcp.tool()
def your_tool(input_data: YourInputModel) -> ToolResponse:
    """Tool wrapper with timing and error handling."""
    start_time = time.time()
    
    try:
        tool = YourTool()
        result = tool.execute_operation(input_data)
        
        execution_time = time.time() - start_time
        return ToolResponse(
            success=True,
            data=result,
            execution_time=execution_time
        )
    except Exception as e:
        execution_time = time.time() - start_time
        return ToolResponse(
            success=False,
            error=ErrorDetail(code="TOOL_ERROR", message=str(e)),
            execution_time=execution_time
        )
```

## 🧪 Testing Strategy

Each tool has comprehensive tests covering:

```python
class TestYourTool:
    @pytest.fixture
    def tool(self):
        tool = YourTool()
        tool.initialize()
        return tool
    
    def test_initialization(self):
        # Test setup process
        pass
    
    def test_health_check(self, tool):
        # Test health validation
        assert tool.health_check() is True
    
    def test_valid_operation(self, tool):
        # Test successful operation
        pass
    
    def test_invalid_input(self, tool):
        # Test error handling
        pass
    
    def test_edge_cases(self, tool):
        # Test boundary conditions
        pass
```

## 🔄 Adding New Tools

### 1. Create Tool Class

```bash
# Create new tool file
touch src/tools/your_tool.py
```

### 2. Implement Core Functionality

Follow the base pattern with:
- Input validation
- Early returns for errors
- Proper logging
- Health check implementation

### 3. Add Pydantic Models

In `src/models.py`:
```python
class YourToolInput(BaseModel):
    # Input parameters with validation
    pass

class YourToolResult(BaseModel):
    # Output structure
    pass
```

### 4. Server Integration

In `src/server.py`:
```python
@mcp.tool()
def your_tool_function(input_data: YourToolInput) -> ToolResponse:
    # Server wrapper implementation
    pass
```

### 5. CLI Integration

In `cli.py`:
```python
@click.group()
def your_tool():
    """Your tool CLI commands."""
    pass

@your_tool.command()
def action(params):
    """Tool action command."""
    # CLI implementation
    pass
```

### 6. Create Tests

```bash
# Add tests
# tests/test_tools.py - add TestYourTool class
```

## 🔒 Security Guidelines

- **Input Validation:** Every input validated with Pydantic
- **Early Returns:** Validate first, process second
- **Error Handling:** Never expose sensitive information
- **Resource Limits:** Enforce timeouts and size limits
- **Logging:** Log operations but not sensitive data
- **Sandboxing:** Restrict file and network access

## 📊 Performance Considerations

- **Initialization:** Lazy loading where possible
- **Caching:** Cache expensive operations with TTL
- **Resource Management:** Clean up properly
- **Async Operations:** Use async/await for I/O bound operations
- **Monitoring:** Include performance metrics

## 🚀 Production Guidelines

- **Configuration:** Use `src/config.py` for all settings
- **Logging:** Structured logging with appropriate levels
- **Error Handling:** Graceful degradation
- **Health Checks:** Implement meaningful health validation
- **Documentation:** Clear docstrings for complex logic
- **Testing:** 80%+ coverage with integration tests