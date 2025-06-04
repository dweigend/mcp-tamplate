"""📁 File Manager Tool - Secure File Operations.

Provides secure file operations with sandboxing, validation, and proper
error handling. All operations are restricted to allowed directories.

Features:
- Read, write, list, and check file operations
- Path traversal protection
- File size limits and validation
- Encoding support with fallback
- Comprehensive error handling

Security:
- Sandboxed to allowed directories only
- Path traversal prevention
- File extension filtering
- Size limits enforced

References:
- Python pathlib for secure path handling
- Coding standards: Early returns, single responsibility
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.config import (
    ALLOWED_READ_PATHS,
    ALLOWED_WRITE_PATHS,
    BLOCKED_EXTENSIONS,
    DATA_DIR,
    FILE_MANAGER_ALLOWED_EXTENSIONS,
    FILE_MANAGER_MAX_FILE_SIZE,
    FILE_MANAGER_SAFE_DIRECTORIES,
)
from src.models import FileInfo, FileManagerResult, FileOperation

logger = logging.getLogger(__name__)


class FileManagerTool:
    """📁 Secure file manager with sandboxing and validation."""
    
    def __init__(self) -> None:
        """Initialize file manager with security settings."""
        self._initialized = False
        self._safe_directories = [Path(d) for d in FILE_MANAGER_SAFE_DIRECTORIES]
        self._allowed_extensions = set(FILE_MANAGER_ALLOWED_EXTENSIONS)
        self._blocked_extensions = set(BLOCKED_EXTENSIONS)
        
        # Operation dispatch map
        self._operations = {
            FileOperation.READ: self._read_file,
            FileOperation.WRITE: self._write_file,
            FileOperation.LIST: self._list_directory,
            FileOperation.EXISTS: self._check_exists,
            FileOperation.DELETE: self._delete_file,
        }
    
    def initialize(self) -> None:
        """🔧 Initialize file manager and create safe directories."""
        if self._initialized:
            return
        
        # Ensure safe directories exist
        for directory in self._safe_directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"📁 Ensured directory exists: {directory}")
        
        self._initialized = True
        logger.info("📁 File manager tool initialized")
    
    def health_check(self) -> bool:
        """💚 Verify file manager is working correctly."""
        try:
            # Check if we can access safe directories
            for directory in self._safe_directories:
                if not directory.exists() or not directory.is_dir():
                    return False
            
            # Test basic file operations
            test_file = DATA_DIR / "health_check.txt"
            test_content = "health check"
            
            # Try write and read
            test_file.write_text(test_content, encoding="utf-8")
            read_content = test_file.read_text(encoding="utf-8")
            test_file.unlink()  # Clean up
            
            return read_content == test_content
            
        except Exception as e:
            logger.error(f"❌ File manager health check failed: {e}")
            return False
    
    def execute_operation(
        self,
        operation: FileOperation,
        path: str,
        content: Optional[str] = None,
        encoding: str = "utf-8"
    ) -> FileManagerResult:
        """📁 Execute file operation with security validation.
        
        Args:
            operation: Type of file operation to perform
            path: Target file or directory path
            content: Content to write (for write operations)
            encoding: File encoding (default: utf-8)
            
        Returns:
            FileManagerResult: Operation result with details
            
        Raises:
            ValueError: For invalid paths or operations
            PermissionError: For unauthorized access attempts
            FileNotFoundError: For missing files/directories
        """
        if not self._initialized:
            self.initialize()
        
        # Validate and normalize path
        safe_path = self._validate_and_normalize_path(path, operation)
        
        # Execute operation
        try:
            operation_func = self._operations[operation]
            return operation_func(safe_path, content, encoding)
            
        except Exception as e:
            logger.error(f"❌ File operation failed: {operation} on {path}: {e}")
            return FileManagerResult(
                operation=operation,
                path=path,
                success=False,
                message=f"Operation failed: {str(e)}"
            )
    
    def _validate_and_normalize_path(self, path: str, operation: FileOperation) -> Path:
        """🔒 Validate path security and normalize to absolute path."""
        if not path or not path.strip():
            raise ValueError("Path cannot be empty")
        
        # Convert to Path object and resolve
        try:
            user_path = Path(path).resolve()
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid path format: {e}")
        
        # Check for path traversal attempts
        if ".." in str(user_path) or str(user_path).startswith(".."):
            raise ValueError("Path traversal attempts not allowed")
        
        # For relative paths, make them relative to DATA_DIR
        if not user_path.is_absolute():
            user_path = (DATA_DIR / path).resolve()
        
        # Verify path is within safe directories
        if not self._is_path_safe(user_path):
            raise PermissionError(f"Access denied: Path outside safe directories")
        
        # Check write permissions for write operations
        if operation in [FileOperation.WRITE, FileOperation.DELETE]:
            if not self._is_write_allowed(user_path):
                raise PermissionError(f"Write access denied: {user_path}")
        
        # Check file extension if it's a file
        if user_path.suffix and not self._is_extension_allowed(user_path.suffix):
            raise ValueError(f"File extension not allowed: {user_path.suffix}")
        
        return user_path
    
    def _is_path_safe(self, path: Path) -> bool:
        """🔒 Check if path is within safe directories."""
        try:
            for safe_dir in self._safe_directories:
                if path.is_relative_to(safe_dir):
                    return True
            return False
        except (ValueError, OSError):
            return False
    
    def _is_write_allowed(self, path: Path) -> bool:
        """✍️ Check if write operations are allowed for this path."""
        try:
            for allowed_path in ALLOWED_WRITE_PATHS:
                if path.is_relative_to(Path(allowed_path)):
                    return True
            return False
        except (ValueError, OSError):
            return False
    
    def _is_extension_allowed(self, extension: str) -> bool:
        """📄 Check if file extension is allowed."""
        if extension.lower() in self._blocked_extensions:
            return False
        
        # If allowed extensions list is empty, allow all (except blocked)
        if not self._allowed_extensions:
            return True
        
        return extension.lower() in self._allowed_extensions
    
    def _read_file(self, path: Path, content: Optional[str], encoding: str) -> FileManagerResult:
        """📖 Read file content with encoding support."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > FILE_MANAGER_MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes (max: {FILE_MANAGER_MAX_FILE_SIZE})")
        
        try:
            file_content = path.read_text(encoding=encoding)
            logger.info(f"📖 Read file: {path} ({len(file_content)} chars)")
            
            return FileManagerResult(
                operation=FileOperation.READ,
                path=str(path),
                success=True,
                content=file_content,
                message=f"Successfully read file ({len(file_content)} characters)"
            )
            
        except UnicodeDecodeError:
            # Try with fallback encoding
            try:
                file_content = path.read_text(encoding="latin-1")
                return FileManagerResult(
                    operation=FileOperation.READ,
                    path=str(path),
                    success=True,
                    content=file_content,
                    message=f"Read with fallback encoding ({len(file_content)} characters)"
                )
            except Exception as e:
                raise ValueError(f"Failed to read file with any encoding: {e}")
    
    def _write_file(self, path: Path, content: Optional[str], encoding: str) -> FileManagerResult:
        """✍️ Write content to file with validation."""
        if content is None:
            raise ValueError("Content required for write operation")
        
        # Check content size
        content_bytes = len(content.encode(encoding))
        if content_bytes > FILE_MANAGER_MAX_FILE_SIZE:
            raise ValueError(f"Content too large: {content_bytes} bytes")
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path.write_text(content, encoding=encoding)
            logger.info(f"✍️ Wrote file: {path} ({len(content)} chars)")
            
            return FileManagerResult(
                operation=FileOperation.WRITE,
                path=str(path),
                success=True,
                message=f"Successfully wrote {len(content)} characters to file"
            )
            
        except Exception as e:
            raise ValueError(f"Failed to write file: {e}")
    
    def _list_directory(self, path: Path, content: Optional[str], encoding: str) -> FileManagerResult:
        """📂 List directory contents with file information."""
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        try:
            files = []
            for item in path.iterdir():
                file_info = self._get_file_info(item)
                files.append(file_info)
            
            # Sort by name
            files.sort(key=lambda f: f.name)
            
            logger.info(f"📂 Listed directory: {path} ({len(files)} items)")
            
            return FileManagerResult(
                operation=FileOperation.LIST,
                path=str(path),
                success=True,
                files=files,
                message=f"Found {len(files)} items in directory"
            )
            
        except Exception as e:
            raise ValueError(f"Failed to list directory: {e}")
    
    def _check_exists(self, path: Path, content: Optional[str], encoding: str) -> FileManagerResult:
        """🔍 Check if file or directory exists."""
        exists = path.exists()
        
        file_info = None
        if exists:
            file_info = self._get_file_info(path)
        
        logger.debug(f"🔍 Checked existence: {path} -> {exists}")
        
        return FileManagerResult(
            operation=FileOperation.EXISTS,
            path=str(path),
            success=True,
            file_info=file_info,
            message=f"Path {'exists' if exists else 'does not exist'}"
        )
    
    def _delete_file(self, path: Path, content: Optional[str], encoding: str) -> FileManagerResult:
        """🗑️ Delete file or directory."""
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        try:
            if path.is_file():
                path.unlink()
                message = "File deleted successfully"
            elif path.is_dir():
                # Only delete empty directories for safety
                if any(path.iterdir()):
                    raise ValueError("Directory not empty (safety restriction)")
                path.rmdir()
                message = "Empty directory deleted successfully"
            else:
                raise ValueError("Path is neither file nor directory")
            
            logger.info(f"🗑️ Deleted: {path}")
            
            return FileManagerResult(
                operation=FileOperation.DELETE,
                path=str(path),
                success=True,
                message=message
            )
            
        except Exception as e:
            raise ValueError(f"Failed to delete: {e}")
    
    def _get_file_info(self, path: Path) -> FileInfo:
        """ℹ️ Get comprehensive file information."""
        try:
            stat = path.stat()
            
            return FileInfo(
                name=path.name,
                path=str(path),
                size=stat.st_size,
                is_directory=path.is_dir(),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                readable=os.access(path, os.R_OK),
                writable=os.access(path, os.W_OK)
            )
            
        except Exception as e:
            # Return minimal info if stat fails
            return FileInfo(
                name=path.name,
                path=str(path),
                size=0,
                is_directory=False,
                modified_time=datetime.now(),
                readable=False,
                writable=False
            )
    
    def get_safe_directories(self) -> List[str]:
        """📋 Get list of safe directories for file operations."""
        return [str(d) for d in self._safe_directories]
    
    def get_allowed_extensions(self) -> List[str]:
        """📋 Get list of allowed file extensions."""
        return list(self._allowed_extensions)