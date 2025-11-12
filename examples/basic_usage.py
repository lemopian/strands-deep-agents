"""
Basic usage example for Strands DeepAgents.

This example demonstrates:
- Creating a simple deep agent
- Using planning tools
- Working with file operations
- Handling multi-step tasks
"""

from strands_deep_agents import create_deep_agent


def main():
    """Demonstrate basic DeepAgent usage."""

    # Optional: Set environment variable to bypass tool consent prompts for demo
    # os.environ["BYPASS_TOOL_CONSENT"] = "true"

    print("=" * 60)
    print("Strands DeepAgents - Basic Usage Example")
    print("=" * 60)
    print()

    # Create a deep agent with default configuration
    agent = create_deep_agent(
        instructions="You are a helpful assistant that excels at planning and executing complex tasks.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        subagents=[
            {
                "name": "general_purpose",
                "description": "A general-purpose sub-agent that can be used for any task.",
                "prompt": "You are a general-purpose sub-agent that can be used for any task.",
            }
        ],
    )

    # Example 1: Simple task with planning
    print("Example 1: Creating a Python script with planning")
    print("-" * 60)

    result = agent(
        """
    Create a Python script called 'calculator.py' that:
    1. Has functions for add, subtract, multiply, and divide
    2. Includes proper docstrings
    3. Has a main function that demonstrates usage

    Please plan this task first, then execute.
    """
    )

    print("Response:", result)
    print()

    # Check the TODOs created
    todos = agent.state.get("todos")
    if todos:
        print("TODOs created by the agent:")
        for todo in todos:
            print(f"  - [{todo['status']}] {todo['content']}")
        print()

    # Example 2: Continue the conversation
    print("Example 2: Adding tests to the script")
    print("-" * 60)

    result = agent(
        """
    Now create a test file called 'test_calculator.py' with unit tests
    for all the calculator functions.
    """
    )

    print("Response:", result)
    print()

    # Example 3: Use the general_purpose sub-agent
    print("Example 3: Using a sub-agent for code review")
    print("-" * 60)

    result = agent(
        """
    Use the general_purpose sub-agent to review the calculator.py file
    and provide feedback on code quality.
    """
    )

    print("Response:", result)
    print()

    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
