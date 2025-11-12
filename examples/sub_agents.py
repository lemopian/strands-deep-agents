"""
Sub-agents example for Strands DeepAgents.

This example demonstrates:
- Creating custom sub-agents with specialized capabilities
- Delegating tasks to appropriate sub-agents
- Using the general_purpose sub-agent for context quarantine
"""

from strands import tool

from strands_deep_agents import SubAgent, create_deep_agent


# Create a custom tool for the code reviewer
@tool
def analyze_complexity(code: str) -> str:
    """
    Analyze the complexity of code (simple mock implementation).

    Args:
        code: The code to analyze

    Returns:
        Complexity analysis results
    """
    lines = code.strip().split("\n")
    num_lines = len(lines)

    if num_lines < 10:
        complexity = "Low"
    elif num_lines < 50:
        complexity = "Medium"
    else:
        complexity = "High"

    return f"Code complexity: {complexity} ({num_lines} lines of code)"


def main():
    """Demonstrate sub-agent usage."""

    # Optional: Set environment variable to bypass tool consent
    # os.environ["BYPASS_TOOL_CONSENT"] = "true"

    print("=" * 60)
    print("Strands DeepAgents - Sub-Agents Example")
    print("=" * 60)
    print()

    # Define specialized sub-agents
    code_reviewer = SubAgent(
        name="code_reviewer",
        description="Expert code reviewer that analyzes code quality, best practices, and potential issues",
        prompt="""You are an expert code reviewer with years of experience.
        Focus on:
        - Code quality and readability
        - Best practices and design patterns
        - Potential bugs or issues
        - Performance considerations
        Provide constructive feedback with specific suggestions.""",
        tools=[analyze_complexity],
    )

    documentation_writer = SubAgent(
        name="documentation_writer",
        description="Technical writer specialized in creating clear, comprehensive documentation",
        prompt="""You are a technical documentation specialist.
        Create clear, well-structured documentation that includes:
        - Clear explanations of functionality
        - Usage examples
        - API references when applicable
        - Proper formatting with markdown""",
    )

    # Create the main deep agent with sub-agents
    agent = create_deep_agent(
        instructions="""You are a senior software engineer who coordinates development tasks.
        Delegate specialized work to the appropriate sub-agents. You should use ./scrapper/ as the working directory.""",
        subagents=[code_reviewer, documentation_writer],
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    # Example: Complex task with delegation
    print("Task: Create a web scraper with code review and documentation")
    print("-" * 60)
    print()

    result = agent(
        """
    Please complete this development task:

    1. Create a Python web scraper (scraper.py) that:
       - Fetches content from a URL
       - Parses HTML to extract specific data
       - Handles errors gracefully

    2. Have the code_reviewer review the code for quality

    3. Have the documentation_writer create a README.md with usage instructions

    Plan this out first, then execute each step.
    """
    )

    print("Agent Response:")
    print(result)
    print()

    # Show the TODOs that were created
    todos = agent.state.get("todos")
    if todos:
        print("\nTask breakdown (TODOs):")
        for todo in todos:
            status_symbol = "✓" if todo["status"] == "completed" else "○"
            print(f"  {status_symbol} {todo['content']} ({todo['status']})")
        print()

    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
