"""
Utility module containing helper functions.

This module provides common utility functions used throughout the application.
"""


def format_greeting(message):
    """
    Format a greeting message with decorative borders.
    
    Args:
        message (str): The message to format
        
    Returns:
        str: The formatted message with decorative borders
    """
    # Calculate the border length based on message length
    border_length = len(message) + 4
    border = "=" * border_length
    
    # Format the message with borders
    formatted = f"{border}\n| {message} |\n{border}"
    
    return formatted


def get_timestamp():
    """
    Get the current timestamp as a formatted string.
    
    Returns:
        str: Current timestamp in ISO format
    """
    from datetime import datetime
    return datetime.now().isoformat()


def validate_input(input_string):
    """
    Validate that input is not empty.
    
    Args:
        input_string (str): The string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if string exists and is not empty after stripping whitespace
    return bool(input_string and input_string.strip())
