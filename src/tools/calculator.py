"""🧮 Calculator Tool - Mathematical Operations with Validation.

Provides safe mathematical operations with proper input validation,
error handling, and configurable precision.

Features:
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (power, modulo)
- Configurable decimal precision
- Division by zero protection
- Input validation and sanitization

References:
- Python decimal module for precision arithmetic
- Pydantic for input validation
- Coding standards: Single responsibility, early returns
"""

from __future__ import annotations

import logging
import math
from decimal import Decimal, getcontext, InvalidOperation
from typing import List

from src.config import CALCULATOR_ALLOWED_OPERATIONS, CALCULATOR_MAX_PRECISION
from src.models import CalculatorResult, OperationType

logger = logging.getLogger(__name__)


class CalculatorTool:
    """🧮 Mathematical calculator with validation and error handling."""
    
    def __init__(self) -> None:
        """Initialize calculator with default settings."""
        self._initialized = False
        self._operations_map = {
            OperationType.ADD: self._add,
            OperationType.SUBTRACT: self._subtract,
            OperationType.MULTIPLY: self._multiply,
            OperationType.DIVIDE: self._divide,
            OperationType.POWER: self._power,
            OperationType.MODULO: self._modulo,
        }
    
    def initialize(self) -> None:
        """🔧 Initialize the calculator tool."""
        if self._initialized:
            return
            
        # Set decimal precision for accurate calculations
        getcontext().prec = CALCULATOR_MAX_PRECISION + 5  # Extra precision for intermediate calculations
        self._initialized = True
        logger.info("🧮 Calculator tool initialized")
    
    def health_check(self) -> bool:
        """💚 Verify calculator is working correctly."""
        try:
            # Simple test calculation
            result = self.calculate(OperationType.ADD, [1.0, 2.0], 2)
            return abs(result.result - 3.0) < 0.001
        except Exception as e:
            logger.error(f"❌ Calculator health check failed: {e}")
            return False
    
    def calculate(
        self, 
        operation: OperationType, 
        numbers: List[float], 
        precision: int = 2
    ) -> CalculatorResult:
        """🧮 Perform mathematical calculation with validation.
        
        Args:
            operation: Type of mathematical operation
            numbers: List of numbers to operate on
            precision: Decimal precision for result (0-15)
            
        Returns:
            CalculatorResult: Formatted calculation result
            
        Raises:
            ValueError: For invalid inputs or operations
            ZeroDivisionError: For division by zero
        """
        if not self._initialized:
            self.initialize()
        
        # Validate inputs
        self._validate_operation(operation)
        self._validate_numbers(numbers, operation) 
        self._validate_precision(precision)
        
        # Perform calculation
        try:
            operation_func = self._operations_map[operation]
            result = operation_func(numbers)
            
            # Format result with specified precision
            formatted_result = self._format_result(result, precision)
            
            logger.debug(f"🧮 Calculated: {operation} on {numbers} = {result}")
            
            return CalculatorResult(
                result=float(result),
                operation=operation,
                input_numbers=numbers,
                formatted_result=formatted_result
            )
            
        except Exception as e:
            logger.error(f"❌ Calculation failed: {operation} on {numbers}: {e}")
            raise
    
    def _validate_operation(self, operation: OperationType) -> None:
        """✅ Validate operation type."""
        if operation not in self._operations_map:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _validate_numbers(self, numbers: List[float], operation: OperationType) -> None:
        """✅ Validate input numbers based on operation."""
        if not numbers:
            raise ValueError("No numbers provided")
        
        if len(numbers) > 10:
            raise ValueError("Too many numbers (max 10)")
        
        # Check for infinity or NaN
        for num in numbers:
            if math.isnan(num):
                raise ValueError("NaN values not allowed")
            if math.isinf(num):
                raise ValueError("Infinite values not allowed")
        
        # Operation-specific validation
        if operation in [OperationType.SUBTRACT, OperationType.DIVIDE, 
                        OperationType.POWER, OperationType.MODULO]:
            if len(numbers) != 2:
                raise ValueError(f"Operation {operation} requires exactly 2 numbers")
        
        # Division by zero check
        if operation == OperationType.DIVIDE and len(numbers) > 1:
            if numbers[1] == 0:
                raise ZeroDivisionError("Cannot divide by zero")
        
        # Modulo by zero check
        if operation == OperationType.MODULO and len(numbers) > 1:
            if numbers[1] == 0:
                raise ZeroDivisionError("Cannot calculate modulo by zero")
    
    def _validate_precision(self, precision: int) -> None:
        """✅ Validate precision parameter."""
        if not isinstance(precision, int):
            raise ValueError("Precision must be an integer")
        
        if precision < 0 or precision > CALCULATOR_MAX_PRECISION:
            raise ValueError(f"Precision must be between 0 and {CALCULATOR_MAX_PRECISION}")
    
    def _add(self, numbers: List[float]) -> Decimal:
        """➕ Add numbers together."""
        result = Decimal('0')
        for num in numbers:
            result += Decimal(str(num))
        return result
    
    def _subtract(self, numbers: List[float]) -> Decimal:
        """➖ Subtract second number from first."""
        if len(numbers) != 2:
            raise ValueError("Subtraction requires exactly 2 numbers")
        
        return Decimal(str(numbers[0])) - Decimal(str(numbers[1]))
    
    def _multiply(self, numbers: List[float]) -> Decimal:
        """✖️ Multiply numbers together."""
        result = Decimal('1')
        for num in numbers:
            result *= Decimal(str(num))
        return result
    
    def _divide(self, numbers: List[float]) -> Decimal:
        """➗ Divide first number by second."""
        if len(numbers) != 2:
            raise ValueError("Division requires exactly 2 numbers")
        
        dividend = Decimal(str(numbers[0]))
        divisor = Decimal(str(numbers[1]))
        
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        try:
            return dividend / divisor
        except InvalidOperation as e:
            raise ValueError(f"Division operation failed: {e}")
    
    def _power(self, numbers: List[float]) -> Decimal:
        """🔺 Raise first number to power of second."""
        if len(numbers) != 2:
            raise ValueError("Power operation requires exactly 2 numbers")
        
        base = Decimal(str(numbers[0]))
        exponent = numbers[1]  # Keep as float for power operation
        
        try:
            # Handle special cases
            if base == 0 and exponent < 0:
                raise ZeroDivisionError("Cannot raise zero to negative power")
            
            # Use Python's built-in power for better handling of edge cases
            result = base ** Decimal(str(exponent))
            return result
            
        except (InvalidOperation, OverflowError) as e:
            raise ValueError(f"Power operation failed: {e}")
    
    def _modulo(self, numbers: List[float]) -> Decimal:
        """🔢 Calculate modulo (remainder) of division."""
        if len(numbers) != 2:
            raise ValueError("Modulo operation requires exactly 2 numbers")
        
        dividend = Decimal(str(numbers[0]))
        divisor = Decimal(str(numbers[1]))
        
        if divisor == 0:
            raise ZeroDivisionError("Cannot calculate modulo by zero")
        
        try:
            return dividend % divisor
        except InvalidOperation as e:
            raise ValueError(f"Modulo operation failed: {e}")
    
    def _format_result(self, result: Decimal, precision: int) -> str:
        """📝 Format result with specified precision."""
        if precision == 0:
            return str(int(result))
        
        # Format with specified decimal places
        format_string = f"{{:.{precision}f}}"
        return format_string.format(float(result))
    
    def get_supported_operations(self) -> List[str]:
        """📋 Get list of supported operations."""
        return list(CALCULATOR_ALLOWED_OPERATIONS)
    
    def get_operation_info(self, operation: OperationType) -> str:
        """ℹ️ Get human-readable information about an operation."""
        info_map = {
            OperationType.ADD: "Addition: Sum all provided numbers",
            OperationType.SUBTRACT: "Subtraction: Subtract second number from first",
            OperationType.MULTIPLY: "Multiplication: Multiply all provided numbers",
            OperationType.DIVIDE: "Division: Divide first number by second",
            OperationType.POWER: "Exponentiation: Raise first number to power of second",
            OperationType.MODULO: "Modulo: Calculate remainder of division",
        }
        
        return info_map.get(operation, f"Unknown operation: {operation}")