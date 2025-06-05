"""📊 Pydantic models for MCP server data validation.

Core data structures for tools, resources, and server components.
Following MCP specifications and clean code principles.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


# =============================================================================
# 🔢 ENUMS
# =============================================================================

class OperationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract" 
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    MODULO = "modulo"


class FileOperation(str, Enum):
    READ = "read"
    WRITE = "write"
    LIST = "list"
    EXISTS = "exists"
    DELETE = "delete"


# =============================================================================
# 🧮 CALCULATOR MODELS  
# =============================================================================

class CalculatorInput(BaseModel):
    operation: OperationType
    numbers: List[float] = Field(min_items=1, max_items=10)
    precision: int = Field(default=2, ge=0, le=15)

    @validator("numbers")
    def validate_numbers(cls, v: List[float], values: Dict[str, Any]) -> List[float]:
        operation = values.get("operation")
        
        # Binary operations need exactly 2 numbers
        binary_ops = {OperationType.SUBTRACT, OperationType.DIVIDE, 
                     OperationType.POWER, OperationType.MODULO}
        if operation in binary_ops and len(v) != 2:
            raise ValueError(f"Operation {operation} requires exactly 2 numbers")
        
        # Division by zero check
        if operation == OperationType.DIVIDE and len(v) > 1 and v[1] == 0:
            raise ValueError("Cannot divide by zero")
            
        return v


class CalculatorResult(BaseModel):
    """Result from calculator operations."""
    result: float
    operation: OperationType
    input_numbers: List[float]
    formatted_result: str


# =============================================================================
# 📁 FILE MANAGER MODELS
# =============================================================================

class FileManagerInput(BaseModel):
    operation: FileOperation
    path: str = Field(min_length=1, max_length=500)
    content: Optional[str] = Field(default=None, max_length=1_000_000)
    encoding: str = "utf-8"

    @validator("path")
    def validate_path(cls, v: str) -> str:
        if ".." in v or v.startswith("/"):
            raise ValueError("Path traversal not allowed")
        return v

    @validator("content")
    def validate_content(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if values.get("operation") == FileOperation.WRITE and v is None:
            raise ValueError("Content required for write operations")
        return v


class FileInfo(BaseModel):
    name: str
    path: str
    size: int = Field(ge=0)
    is_directory: bool
    modified_time: datetime
    readable: bool
    writable: bool


class FileManagerResult(BaseModel):
    """Result from file manager operations."""
    operation: FileOperation
    path: str
    content: Optional[str] = None
    files: Optional[List[FileInfo]] = None
    file_info: Optional[FileInfo] = None
    message: str


# =============================================================================
# 🔍 SEARCH MODELS
# =============================================================================

class SearchQuery(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    domains: List[str] = Field(default_factory=list, max_items=10)
    limit: int = Field(default=10, ge=1, le=100)
    language: str = Field(default="en", min_length=2, max_length=5)

    @validator("domains")
    def validate_domains(cls, v: List[str]) -> List[str]:
        for domain in v:
            if not domain or "." not in domain:
                raise ValueError(f"Invalid domain format: {domain}")
        return [domain.lower() for domain in v]


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    domain: str
    relevance_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Search results response."""
    query: str
    results: List[SearchResult]
    total_found: int = Field(ge=0)


# =============================================================================
# 🚨 ERROR AND RESPONSE MODELS
# =============================================================================

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    traceback: Optional[str] = None


# ToolResponse removed - FastMCP handles tool responses automatically


# =============================================================================
# ⚙️ SERVER MODELS
# =============================================================================

class ServerInfo(BaseModel):
    """Server information for resources."""
    name: str
    version: str
    description: str
    capabilities: List[str]
    tools_count: int = Field(ge=0)
    uptime: float = Field(ge=0.0)
    status: str = "running"


class HealthCheck(BaseModel):
    """Health check status for resources."""
    status: str = "healthy"
    checks: Dict[str, bool] = Field(default_factory=dict)
    response_time: float = Field(ge=0.0)