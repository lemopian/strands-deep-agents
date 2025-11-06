"""
Calculator Module

A simple calculator module providing basic arithmetic operations with proper
error handling and validation.

Functions:
    add(a, b): Add two numbers
    subtract(a, b): Subtract b from a
    multiply(a, b): Multiply two numbers
    divide(a, b): Divide a by b

Example:
    >>> import calculator
    >>> calculator.add(5, 3)
    8
    >>> calculator.divide(10, 2)
    5.0
"""


def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a (int or float): The first number
        b (int or float): The second number
    
    Returns:
        int or float: The sum of a and b
    
    Raises:
        TypeError: If either argument is not a number
    
    Example:
        >>> add(5, 3)
        8
        >>> add(2.5, 3.7)
        6.2
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers (int or float)")
    
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("Boolean values are not supported")
    
    return a + b


def subtract(a, b):
    """
    Subtract b from a.
    
    Args:
        a (int or float): The number to subtract from
        b (int or float): The number to subtract
    
    Returns:
        int or float: The difference of a and b (a - b)
    
    Raises:
        TypeError: If either argument is not a number
    
    Example:
        >>> subtract(10, 3)
        7
        >>> subtract(5.5, 2.3)
        3.2
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers (int or float)")
    
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("Boolean values are not supported")
    
    return a - b


def multiply(a, b):
    """
    Multiply two numbers together.
    
    Args:
        a (int or float): The first number
        b (int or float): The second number
    
    Returns:
        int or float: The product of a and b
    
    Raises:
        TypeError: If either argument is not a number
    
    Example:
        >>> multiply(5, 3)
        15
        >>> multiply(2.5, 4)
        10.0
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers (int or float)")
    
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("Boolean values are not supported")
    
    return a * b


def divide(a, b):
    """
    Divide a by b.
    
    Args:
        a (int or float): The dividend (number to be divided)
        b (int or float): The divisor (number to divide by)
    
    Returns:
        float: The quotient of a divided by b
    
    Raises:
        TypeError: If either argument is not a number
        ZeroDivisionError: If b is zero
    
    Example:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 2)
        3.5
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers (int or float)")
    
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("Boolean values are not supported")
    
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    
    return a / b


if __name__ == "__main__":
    # Demo usage
    print("Calculator Module Demo")
    print("=" * 40)
    
    print(f"add(5, 3) = {add(5, 3)}")
    print(f"subtract(10, 3) = {subtract(10, 3)}")
    print(f"multiply(4, 7) = {multiply(4, 7)}")
    print(f"divide(15, 3) = {divide(15, 3)}")
    
    print("\nError handling examples:")
    try:
        divide(10, 0)
    except ZeroDivisionError as e:
        print(f"divide(10, 0) raised: {e}")
    
    try:
        add("5", 3)
    except TypeError as e:
        print(f"add('5', 3) raised: {e}")
