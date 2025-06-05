"""🧪 MCP Template CLI - Local Testing Tool.

Command-line interface for testing MCP server tools locally without
requiring Claude Desktop or other MCP clients.

Features:
- Direct tool testing with validation
- Interactive command-line interface
- JSON output formatting
- Error handling and debugging
- Performance timing

Usage:
    python cli.py                           # Interactive mode
    python cli.py calculate --help          # Tool-specific help
    python cli.py calculate add 2 3         # Direct calculation
    python cli.py file read data/test.txt   # File operation
    python cli.py search "python tutorial"  # Web search

References:
- Click documentation for CLI framework
- MCP tools testing patterns
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import click
except ImportError:
    print("❌ Click is required for the CLI tool. Install with: uv add --dev click")
    sys.exit(1)

from pydantic import ValidationError

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.models import (
    CalculatorInput,
    FileManagerInput,
    FileOperation,
    OperationType,
    SearchQuery,
)
from src.tools.calculator import CalculatorTool
from src.tools.file_manager import FileManagerTool
from src.tools.search import SearchTool


# =============================================================================
# 🎨 CLI STYLING AND HELPERS
# =============================================================================

def print_banner() -> None:
    """🎨 Print CLI banner."""
    click.echo("""
🧪 MCP Template CLI - Local Testing Tool
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test your MCP server tools locally before deployment.
""")


def print_success(message: str) -> None:
    """✅ Print success message."""
    click.echo(click.style(f"✅ {message}", fg="green"))


def print_error(message: str) -> None:
    """❌ Print error message."""
    click.echo(click.style(f"❌ {message}", fg="red"))


def print_info(message: str) -> None:
    """ℹ️ Print info message."""
    click.echo(click.style(f"ℹ️  {message}", fg="blue"))


def print_result(result: Any, execution_time: float) -> None:
    """📊 Print formatted result with timing."""
    click.echo(click.style(f"\n📊 Result (took {execution_time:.3f}s):", fg="cyan"))
    
    if hasattr(result, 'dict'):
        # Pydantic model
        formatted = json.dumps(result.dict(), indent=2, default=str)
    elif isinstance(result, dict):
        formatted = json.dumps(result, indent=2, default=str)
    else:
        formatted = str(result)
    
    click.echo(formatted)


# =============================================================================
# 🧮 CALCULATOR COMMANDS
# =============================================================================

@click.group()
def calculator() -> None:
    """🧮 Mathematical calculator tool commands."""
    pass


@calculator.command()
@click.argument("operation", type=click.Choice(["add", "subtract", "multiply", "divide", "power", "modulo"]))
@click.argument("numbers", nargs=-1, type=float, required=True)
@click.option("--precision", "-p", type=int, default=2, help="Decimal precision (0-15)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def calculate(operation: str, numbers: tuple, precision: int, output_json: bool) -> None:
    """🧮 Perform mathematical calculations.
    
    Examples:
        cli.py calculator calculate add 2 3 5
        cli.py calculator calculate divide 10 3 --precision 4
        cli.py calculator calculate power 2 8
    """
    try:
        # Convert to list and create input model
        numbers_list = list(numbers)
        if DEBUG_MODE:
            click.echo(f"Debug: numbers={numbers}, numbers_list={numbers_list}")
        calc_input = CalculatorInput(
            operation=OperationType(operation),
            numbers=numbers_list,
            precision=precision
        )
        
        # Execute calculation
        calc_tool = CalculatorTool()
        calc_tool.initialize()
        
        start_time = time.time()
        result = calc_tool.calculate(
            operation=calc_input.operation,
            numbers=calc_input.numbers,
            precision=calc_input.precision
        )
        execution_time = time.time() - start_time
        
        if output_json:
            print_result(result, execution_time)
        else:
            print_success(f"Calculation: {operation} on {numbers_list}")
            click.echo(f"Result: {result.formatted_result}")
            click.echo(f"Execution time: {execution_time:.3f}s")
        
    except ValidationError as e:
        print_error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Calculation failed: {e}")
        sys.exit(1)


@calculator.command()
def operations() -> None:
    """📋 List supported mathematical operations."""
    calc_tool = CalculatorTool()
    calc_tool.initialize()
    
    operations_list = calc_tool.get_supported_operations()
    
    click.echo("🧮 Supported Operations:")
    for op in operations_list:
        try:
            op_type = OperationType(op)
            info = calc_tool.get_operation_info(op_type)
            click.echo(f"  • {op}: {info}")
        except ValueError:
            click.echo(f"  • {op}: Operation")


# =============================================================================
# 📁 FILE MANAGER COMMANDS
# =============================================================================

@click.group()
def file() -> None:
    """📁 File manager tool commands."""
    pass


@file.command()
@click.argument("path", type=str)
@click.option("--encoding", default="utf-8", help="File encoding")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def read(path: str, encoding: str, output_json: bool) -> None:
    """📖 Read file content.
    
    Example:
        cli.py file read data/example.txt
        cli.py file read data/config.json --encoding utf-8
    """
    try:
        file_input = FileManagerInput(
            operation=FileOperation.READ,
            path=path,
            encoding=encoding
        )
        
        file_tool = FileManagerTool()
        file_tool.initialize()
        
        start_time = time.time()
        result = file_tool.execute_operation(
            operation=file_input.operation,
            path=file_input.path,
            encoding=file_input.encoding
        )
        execution_time = time.time() - start_time
        
        if output_json:
            print_result(result, execution_time)
        else:
            if result.success:
                print_success(f"Read file: {path}")
                if result.content:
                    click.echo(f"\nContent:\n{result.content}")
            else:
                print_error(f"Failed to read file: {result.message}")
                sys.exit(1)
        
    except ValidationError as e:
        print_error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"File operation failed: {e}")
        sys.exit(1)


@file.command()
@click.argument("path", type=str)
@click.argument("content", type=str)
@click.option("--encoding", default="utf-8", help="File encoding")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def write(path: str, content: str, encoding: str, output_json: bool) -> None:
    """✍️ Write content to file.
    
    Example:
        cli.py file write data/test.txt "Hello, World!"
        cli.py file write data/config.json '{"key": "value"}'
    """
    try:
        file_input = FileManagerInput(
            operation=FileOperation.WRITE,
            path=path,
            content=content,
            encoding=encoding
        )
        
        file_tool = FileManagerTool()
        file_tool.initialize()
        
        start_time = time.time()
        result = file_tool.execute_operation(
            operation=file_input.operation,
            path=file_input.path,
            content=file_input.content,
            encoding=file_input.encoding
        )
        execution_time = time.time() - start_time
        
        if output_json:
            print_result(result, execution_time)
        else:
            if result.success:
                print_success(f"Wrote to file: {path}")
                click.echo(f"Characters written: {len(content)}")
            else:
                print_error(f"Failed to write file: {result.message}")
                sys.exit(1)
        
    except ValidationError as e:
        print_error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"File operation failed: {e}")
        sys.exit(1)


@file.command()
@click.argument("path", type=str)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def list(path: str, output_json: bool) -> None:
    """📂 List directory contents.
    
    Example:
        cli.py file list data/
        cli.py file list . --json
    """
    try:
        file_input = FileManagerInput(
            operation=FileOperation.LIST,
            path=path
        )
        
        file_tool = FileManagerTool()
        file_tool.initialize()
        
        start_time = time.time()
        result = file_tool.execute_operation(
            operation=file_input.operation,
            path=file_input.path
        )
        execution_time = time.time() - start_time
        
        if output_json:
            print_result(result, execution_time)
        else:
            if result.success and result.files:
                print_success(f"Listed directory: {path}")
                click.echo(f"\nFound {len(result.files)} items:")
                for file_info in result.files:
                    icon = "📁" if file_info.is_directory else "📄"
                    size = f"({file_info.size} bytes)" if not file_info.is_directory else ""
                    click.echo(f"  {icon} {file_info.name} {size}")
            else:
                print_error(f"Failed to list directory: {result.message}")
                sys.exit(1)
        
    except ValidationError as e:
        print_error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"File operation failed: {e}")
        sys.exit(1)


@file.command()
def safe_dirs() -> None:
    """📋 List safe directories for file operations."""
    file_tool = FileManagerTool()
    file_tool.initialize()
    
    safe_dirs = file_tool.get_safe_directories()
    
    click.echo("📁 Safe Directories for File Operations:")
    for directory in safe_dirs:
        click.echo(f"  • {directory}")


# =============================================================================
# 🔍 SEARCH COMMANDS
# =============================================================================

@click.group()
def search() -> None:
    """🔍 Web search tool commands."""
    pass


@search.command()
@click.argument("query", type=str)
@click.option("--limit", "-l", type=int, default=10, help="Maximum results (1-100)")
@click.option("--domains", "-d", multiple=True, help="Domain filters (can specify multiple)")
@click.option("--language", default="en", help="Search language code")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def web(query: str, limit: int, domains: tuple, language: str, output_json: bool) -> None:
    """🔍 Search the web with optional filtering.
    
    Examples:
        cli.py search web "python tutorial"
        cli.py search web "machine learning" --limit 5
        cli.py search web "API documentation" -d docs.python.org -d github.com
    """
    try:
        search_query = SearchQuery(
            text=query,
            domains=list(domains),
            limit=limit,
            language=language
        )
        
        search_tool = SearchTool()
        search_tool.initialize()
        
        start_time = time.time()
        result = search_tool.search(
            text=search_query.text,
            domains=search_query.domains,
            limit=search_query.limit,
            language=search_query.language
        )
        execution_time = time.time() - start_time
        
        if output_json:
            print_result(result, execution_time)
        else:
            print_success(f"Search completed: '{query}'")
            click.echo(f"Found {result.total_found} results in {result.search_time:.3f}s\n")
            
            for i, search_result in enumerate(result.results, 1):
                click.echo(f"{i}. {search_result.title}")
                click.echo(f"   🔗 {search_result.url}")
                click.echo(f"   📝 {search_result.snippet}")
                if search_result.relevance_score:
                    click.echo(f"   📊 Relevance: {search_result.relevance_score:.2f}")
                click.echo()
        
    except ValidationError as e:
        print_error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Search failed: {e}")
        sys.exit(1)


@search.command()
def info() -> None:
    """ℹ️ Show search tool capabilities and limits."""
    search_tool = SearchTool()
    search_tool.initialize()
    
    info = search_tool.get_search_info()
    
    click.echo("🔍 Search Tool Information:")
    for key, value in info.items():
        click.echo(f"  • {key.replace('_', ' ').title()}: {value}")


# =============================================================================
# 🧪 HEALTH AND TESTING COMMANDS
# =============================================================================

@click.command()
def health() -> None:
    """💚 Check health of all tools."""
    print_info("Performing health checks...")
    
    tools = [
        ("Calculator", CalculatorTool()),
        ("File Manager", FileManagerTool()),
        ("Search", SearchTool())
    ]
    
    all_healthy = True
    
    for name, tool in tools:
        try:
            tool.initialize()
            is_healthy = tool.health_check()
            
            if is_healthy:
                print_success(f"{name} tool: Healthy")
            else:
                print_error(f"{name} tool: Unhealthy")
                all_healthy = False
                
        except Exception as e:
            print_error(f"{name} tool: Error - {e}")
            all_healthy = False
    
    if all_healthy:
        print_success("All tools are healthy! 🎉")
    else:
        print_error("Some tools have issues.")
        sys.exit(1)


@click.command()
def demo() -> None:
    """🎯 Run demonstration of all tools."""
    print_info("Running tool demonstrations...")
    
    # Calculator demo
    click.echo("\n🧮 Calculator Demo:")
    try:
        calc_tool = CalculatorTool()
        calc_tool.initialize()
        result = calc_tool.calculate(OperationType.ADD, [2.0, 3.0, 5.0], 2)
        click.echo(f"  2 + 3 + 5 = {result.formatted_result}")
    except Exception as e:
        print_error(f"Calculator demo failed: {e}")
    
    # File Manager demo
    click.echo("\n📁 File Manager Demo:")
    try:
        file_tool = FileManagerTool()
        file_tool.initialize()
        
        # Test write and read
        test_content = "Hello from MCP Template!"
        write_result = file_tool.execute_operation(
            FileOperation.WRITE, 
            "data/demo_file.txt", 
            test_content
        )
        
        if write_result.success:
            read_result = file_tool.execute_operation(
                FileOperation.READ,
                "data/demo_file.txt"
            )
            if read_result.success:
                click.echo(f"  Written and read: '{read_result.content}'")
        
    except Exception as e:
        print_error(f"File manager demo failed: {e}")
    
    # Search demo
    click.echo("\n🔍 Search Demo:")
    try:
        search_tool = SearchTool()
        search_tool.initialize()
        result = search_tool.search("python", limit=2)
        click.echo(f"  Found {len(result.results)} results for 'python'")
        if result.results:
            click.echo(f"  First result: {result.results[0].title}")
            
    except Exception as e:
        print_error(f"Search demo failed: {e}")
    
    print_success("Demo completed!")


# =============================================================================
# 🚀 MAIN CLI GROUP
# =============================================================================

@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """🧪 MCP Template CLI - Local Testing Tool
    
    Test your MCP server tools locally before deployment.
    Use --help with any command for detailed usage information.
    """
    pass


# Add command groups
cli.add_command(calculator)
cli.add_command(file)
cli.add_command(search)
cli.add_command(health)
cli.add_command(demo)


@cli.command()
def interactive() -> None:
    """🎮 Interactive mode for testing tools."""
    print_banner()
    print_info("Interactive mode - type 'help' for commands")
    
    while True:
        try:
            command = click.prompt("\n🧪 MCP CLI", type=str).strip()
            
            if command.lower() in ["exit", "quit", "q"]:
                print_info("Goodbye!")
                break
            elif command.lower() in ["help", "h"]:
                click.echo("""
Available commands:
  🧮 calc add 2 3        - Calculator operations
  📁 file read test.txt  - File operations  
  🔍 search python      - Web search
  💚 health             - Health check
  🎯 demo               - Run demonstrations
  ❓ help               - Show this help
  🚪 exit               - Exit interactive mode
""")
            elif command.lower() == "health":
                ctx = click.Context(health)
                health.invoke(ctx)
            elif command.lower() == "demo":
                ctx = click.Context(demo)
                demo.invoke(ctx)
            else:
                # Try to parse as CLI command
                try:
                    args = command.split()
                    if args[0] == "calc" and len(args) >= 3:
                        # Calculator shorthand
                        operation = args[1]
                        numbers = [float(x) for x in args[2:]]
                        calc_tool = CalculatorTool()
                        calc_tool.initialize()
                        result = calc_tool.calculate(OperationType(operation), numbers)
                        click.echo(f"Result: {result.formatted_result}")
                    else:
                        print_error("Unknown command. Type 'help' for available commands.")
                except Exception as e:
                    print_error(f"Command failed: {e}")
                    
        except KeyboardInterrupt:
            print_info("\nGoodbye!")
            break
        except EOFError:
            print_info("\nGoodbye!")
            break


def main() -> None:
    """🚀 Main CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        print_info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"CLI error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()