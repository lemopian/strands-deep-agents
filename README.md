# Hello World Python Project

A simple Python project demonstrating basic project structure with functions and unit tests.

## Project Structure

```
.
├── main.py              # Main module with hello world functions
├── tests/               # Test directory
│   ├── __init__.py     # Makes tests a package
│   └── test_main.py    # Unit tests for main module
└── README.md           # This file
```

## Features

This project includes:
- A `hello_world()` function that returns a simple greeting
- A `greet(name)` function that returns a personalized greeting
- Comprehensive unit tests using Python's unittest framework

## Installation

No external dependencies are required. This project uses only Python standard library.

### Requirements
- Python 3.6 or higher

## Usage

### Running the Main Script

To run the main script directly:

```bash
python main.py
```

This will output:
```
Hello, World!
Hello, Python Developer!
```

### Using the Functions in Your Code

You can import and use the functions in your own code:

```python
from main import hello_world, greet

# Get a simple greeting
message = hello_world()
print(message)  # Output: Hello, World!

# Get a personalized greeting
personalized = greet("Alice")
print(personalized)  # Output: Hello, Alice!
```

## Running Tests

To run all unit tests:

```bash
python -m unittest discover tests
```

To run a specific test file:

```bash
python -m unittest tests.test_main
```

To run tests with verbose output:

```bash
python -m unittest discover tests -v
```

Alternatively, you can run the test file directly:

```bash
python tests/test_main.py
```

## Functions

### `hello_world()`

Returns a simple "Hello, World!" greeting.

**Returns:** `str` - A greeting message

**Example:**
```python
>>> hello_world()
'Hello, World!'
```

### `greet(name)`

Returns a personalized greeting for the given name.

**Parameters:**
- `name` (str): The name to include in the greeting

**Returns:** `str` - A personalized greeting message

**Example:**
```python
>>> greet("Alice")
'Hello, Alice!'
```

## Testing

The project includes comprehensive unit tests covering:
- Basic functionality of `hello_world()`
- Return type validation
- Personalized greetings with the `greet()` function
- Multiple test cases for different inputs

## License

This is a sample project for educational purposes.

## Contributing

Feel free to fork this project and experiment with it!
