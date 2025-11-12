"""
Example demonstrating sequential tool execution in DeepAgents.

This example shows how to use the disable_parallel_tool_calling parameter
to force sequential execution of tools and sub-agents, which can be useful
for debugging or when tools have dependencies on each other.
"""

from strands_deep_agents import create_deep_agent


def main():
    """Demonstrate sequential tool execution."""

    print("=" * 70)
    print("Sequential Tool Execution Example")
    print("=" * 70)
    print()

    # Example 1: Agent with parallel execution (default)
    print("Example 1: Agent with parallel tool calling (default)")
    print("-" * 70)

    agent_parallel = create_deep_agent(
        instructions="You are a helpful assistant.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
    )

    print(f"Tool executor: {type(agent_parallel.tool_executor).__name__}")
    print("This agent can execute multiple tools in parallel.")
    print()

    # Example 2: Agent with sequential execution
    print("Example 2: Agent with sequential tool calling")
    print("-" * 70)

    agent_sequential = create_deep_agent(
        instructions="You are a helpful assistant.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        disable_parallel_tool_calling=True,
    )

    print(f"Tool executor: {type(agent_sequential.tool_executor).__name__}")
    print("This agent will execute tools one at a time, sequentially.")
    print()

    # Example 3: Agent with sub-agents and sequential execution
    print("Example 3: Agent with sub-agents and sequential execution")
    print("-" * 70)

    code_reviewer = {
        "name": "code_reviewer",
        "description": "Reviews code for quality and best practices",
        "prompt": "You are an expert code reviewer with deep knowledge of best practices.",
    }

    test_writer = {
        "name": "test_writer",
        "description": "Writes comprehensive unit tests",
        "prompt": "You are an expert at writing thorough unit tests.",
    }

    agent_with_subagents = create_deep_agent(
        instructions="You are a senior developer managing code quality.",
        model="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        subagents=[code_reviewer, test_writer],
        disable_parallel_tool_calling=True,
    )

    print(f"Main agent tool executor: {type(agent_with_subagents.tool_executor).__name__}")
    print("Sub-agents will also use sequential execution.")
    print("This ensures predictable, step-by-step execution.")
    print()

    print("=" * 70)
    print("Use Cases for Sequential Execution:")
    print("-" * 70)
    print("1. Debugging: Easier to trace execution flow")
    print("2. Dependencies: When tools must run in specific order")
    print("3. Resource constraints: Limited concurrent API calls")
    print("4. Deterministic behavior: Same order every time")
    print("=" * 70)


if __name__ == "__main__":
    main()
