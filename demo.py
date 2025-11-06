#!/usr/bin/env python3
"""
Quick demo of Strands DeepAgents capabilities.

This script demonstrates the core features of DeepAgents:
- Automatic planning with TODOs
- File operations
- Sub-agent delegation
- Multi-step task execution

Run: python demo.py
"""

import os
import sys


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---\n")


def check_environment():
    """Check if the environment is properly configured."""
    print_section("Environment Check")

    issues = []

    # Check for strands installation
    try:
        import strands

        print("✓ strands-agents installed")
    except ImportError:
        issues.append("strands-agents not installed. Run: pip install strands-agents")

    # Check for strands-tools
    try:
        import strands_tools

        print("✓ strands-agents-tools installed")
    except ImportError:
        print("⚠ strands-agents-tools not installed (optional but recommended)")
        print("  Install with: pip install strands-agents-tools")

    # Check for credentials
    has_creds = False
    if os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"):
        print("✓ AWS credentials configured")
        has_creds = True
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("✓ Anthropic API key configured")
        has_creds = True
    elif os.getenv("OPENAI_API_KEY"):
        print("✓ OpenAI API key configured")
        has_creds = True

    if not has_creds:
        issues.append(
            "No model provider credentials found. Set one of:\n"
            "  - AWS_REGION (for Bedrock)\n"
            "  - ANTHROPIC_API_KEY (for Anthropic)\n"
            "  - OPENAI_API_KEY (for OpenAI)"
        )

    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("\n✓ All checks passed!")
    return True


def demo_basic_planning():
    """Demonstrate basic planning capability."""
    from strands_deepagents import create_deep_agent

    print_section("Demo 1: Basic Planning")

    agent = create_deep_agent(
        instructions="You are a helpful assistant that breaks down complex tasks.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    print("Task: Create a simple calculator Python module")
    print()

    result = agent(
        """
    Create a calculator module with:
    1. Add, subtract, multiply, divide functions
    2. Proper error handling
    3. Docstrings
    
    Please plan this first using TODOs, then execute.
    """
    )

    print_subsection("Agent Response")
    print(result)

    # Show the plan
    todos = agent.state.get("todos")
    if todos:
        print_subsection("Agent's Plan")
        for todo in todos:
            status_icon = {
                "completed": "✅",
                "in_progress": "🔄",
                "pending": "⏳",
            }.get(todo["status"], "❓")
            print(f"  {status_icon} {todo['content']}")


def demo_sub_agents():
    """Demonstrate sub-agent usage."""
    from strands_deepagents import create_deep_agent, SubAgent

    print_section("Demo 2: Sub-Agent Delegation")

    # Create a specialized sub-agent
    reviewer = SubAgent(
        name="code_reviewer",
        description="Specialized in reviewing code quality and best practices",
        instructions="""You are an expert code reviewer.
        Focus on:
        - Code quality and readability
        - Potential bugs or issues
        - Best practices
        Provide specific, actionable feedback.""",
    )

    agent = create_deep_agent(
        instructions="You are a senior developer who writes code and coordinates reviews.",
        sub_agents=[reviewer],
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    print("Task: Write a function and have it reviewed")
    print()

    result = agent(
        """
    Write a Python function to check if a string is a palindrome,
    then have the code_reviewer analyze it for quality.
    """
    )

    print_subsection("Agent Response")
    print(result)


def demo_file_operations():
    """Demonstrate file operations."""
    from strands_deepagents import create_deep_agent

    print_section("Demo 3: File Operations")

    agent = create_deep_agent(
        instructions="You are a helpful assistant that works with files.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    print("Task: Create a mini project structure")
    print()

    result = agent(
        """
    Create a basic Python project structure:
    1. main.py - Entry point with a hello world function
    2. utils.py - A utility module with a helper function
    3. README.md - Project documentation
    
    Keep it simple and include comments.
    """
    )

    print_subsection("Agent Response")
    print(result)


def main():
    """Run the demo."""
    print_section("Strands DeepAgents Demo")
    print("This demo showcases the core capabilities of DeepAgents.")
    print()
    print("Press Ctrl+C at any time to exit.")

    # Check environment
    if not check_environment():
        print("\nPlease fix the issues above and try again.")
        return 1

    # Set bypass for demo
    os.environ["BYPASS_TOOL_CONSENT"] = "true"

    try:
        # Run demos
        demo_basic_planning()

        input("\nPress Enter to continue to the next demo...")
        demo_sub_agents()

        input("\nPress Enter to continue to the next demo...")
        demo_file_operations()

        print_section("Demo Complete!")
        print("Explore more examples in the examples/ directory.")
        print("Read QUICKSTART.md for more information.")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return 0
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        print("\nThis might be due to:")
        print("  - Missing API credentials")
        print("  - Network connectivity issues")
        print("  - API rate limits")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
