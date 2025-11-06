"""
Main entry point for the application.

This module serves as the primary entry point for the program.
"""

from utils import format_greeting


def hello_world():
    """
    Main hello world function.
    
    Returns:
        str: A greeting message
    """
    message = "Hello, World!"
    formatted_message = format_greeting(message)
    return formatted_message


def main():
    """
    Main function to run the application.
    """
    # Print the greeting message
    greeting = hello_world()
    print(greeting)
    
    # Additional example usage
    custom_greeting = format_greeting("Welcome to Python!")
    print(custom_greeting)


if __name__ == "__main__":
    # This block runs when the script is executed directly
    main()
