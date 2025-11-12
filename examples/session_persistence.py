"""
Session Persistence Example for Strands DeepAgents.

This example demonstrates:
- Creating agents with session persistence
- Recovering from failures using FileSessionManager
- Maintaining conversation history across sessions
- Persisting agent state (todos, custom state)
"""

from datetime import date
from pathlib import Path

from strands.session.file_session_manager import FileSessionManager

from strands_deep_agents import create_deep_agent


def example_basic_session_persistence():
    """
    Demonstrate basic session persistence with conversation history.
    """
    print("=" * 70)
    print("Example 1: Basic Session Persistence")
    print("=" * 70)
    print()

    session_id = f"example-{date.today().isoformat()}"
    storage_dir = "./.agent_sessions"

    # Create session manager
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    # Create agent with session persistence
    agent = create_deep_agent(
        instructions="You are a helpful assistant that remembers previous conversations.",
        session_manager=session_manager,
    )

    # First interaction
    print("First interaction:")
    result = agent("Hello, my name is Pierre Ange and I love France and Cameroun 🇨🇲🇫🇷.")
    print(f"Agent: {result}")
    print()

    # Second interaction in the same session
    print("Second interaction (same agent instance):")
    result = agent("What's my name and what do I love?")
    print(f"Agent: {result}")
    print()

    # Simulate creating a new agent instance (e.g., after app restart)
    print("Third interaction (simulating app restart with new agent instance):")
    session_manager_restored = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    agent_restored = create_deep_agent(
        instructions="You are a helpful assistant that remembers previous conversations.",
        session_manager=session_manager_restored,
    )

    # The agent should remember the previous conversation
    result = agent_restored("Can you remind me what we discussed earlier?")
    print(f"Agent (restored): {result}")
    print()

    # Show session storage location
    session_path = Path(storage_dir) / f"session_{session_id}"
    print(f"Session data stored at: {session_path}")
    print()


def example_failure_recovery():
    """
    Demonstrate recovery from failure using session persistence.
    """
    print("=" * 70)
    print("Example 2: Failure Recovery with Session Persistence")
    print("=" * 70)
    print()

    session_id = "example-task-session"
    storage_dir = "./.agent_sessions"

    # Create session manager
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    # Create agent with session persistence
    agent = create_deep_agent(
        instructions="You are a coding assistant that helps with multi-step tasks.",
        session_manager=session_manager,
    )

    # Start a complex task
    print("Starting a multi-step task:")
    result = agent(
        """
        I need you to create a simple Python project with:
        1. A main.py file with a hello world function
        2. A tests directory with test files
        3. A README.md explaining the project

        Please create a plan first using todos.
        """
    )
    print(f"Agent: {result}")
    print()

    # Check todos
    todos = agent.state.get("todos")
    if todos:
        print("TODOs created:")
        for todo in todos:
            print(f"  - [{todo['status']}] {todo['content']}")
        print()

    # Simulate a failure by creating a new agent instance mid-task
    print("Simulating failure... Creating new agent instance with same session:")
    session_manager_recovered = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    agent_recovered = create_deep_agent(
        instructions="You are a coding assistant that helps with multi-step tasks.",
        session_manager=session_manager_recovered,
    )

    # The agent should remember the task and continue
    print("Recovered agent checking status:")
    result = agent_recovered("What task was I working on? Show me the current status.")
    print(f"Agent (recovered): {result}")
    print()

    # Continue with the task
    print("Continuing the task:")
    result = agent_recovered("Please continue with the next step in the plan.")
    print(f"Agent: {result}")
    print()


def example_state_persistence():
    """
    Demonstrate persistence of custom agent state.
    """
    print("=" * 70)
    print("Example 3: Custom State Persistence")
    print("=" * 70)
    print()

    session_id = "example-state-session"
    storage_dir = "./.agent_sessions"

    # Create agent with initial state
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    agent = create_deep_agent(
        instructions="You are a helpful assistant.",
        initial_state={
            "user_preferences": {"theme": "dark", "language": "python"},
            "task_count": 0,
        },
        session_manager=session_manager,
    )

    # Interact and modify state
    print("Setting user preferences:")
    agent.state.set("user_preferences", {"theme": "light", "language": "javascript"})
    agent.state.set("task_count", 5)
    print(f"Theme: {agent.state.get('user_preferences')['theme']}")
    print(f"Task count: {agent.state.get('task_count')}")
    print()

    # Have a conversation
    result = agent("Remember that I prefer TypeScript for new projects.")
    print(f"Agent: {result}")
    print()

    # Create new agent instance with same session
    print("Creating new agent instance (simulating restart):")
    session_manager_restored = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    agent_restored = create_deep_agent(
        instructions="You are a helpful assistant.",
        session_manager=session_manager_restored,
    )

    # Check that state was restored
    print("Restored state:")
    print(f"Theme: {agent_restored.state.get('user_preferences')['theme']}")
    print(f"Task count: {agent_restored.state.get('task_count')}")
    print()

    # Check conversation history
    result = agent_restored("What language do I prefer for new projects?")
    print(f"Agent (restored): {result}")
    print()


def cleanup_sessions():
    """
    Clean up example session data.
    """
    storage_dir = Path("./.agent_sessions")
    if storage_dir.exists():
        import shutil

        shutil.rmtree(storage_dir)
        print(f"Cleaned up session data at {storage_dir}")


def main():
    """
    Run all session persistence examples.
    """
    print("\n")
    print("█" * 70)
    print("  Strands DeepAgents - Session Persistence Examples")
    print("█" * 70)
    print("\n")

    try:
        # Run examples
        example_basic_session_persistence()
        input("\nPress Enter to continue to the next example...\n")

        example_failure_recovery()
        input("\nPress Enter to continue to the next example...\n")

        example_state_persistence()

        print("\n")
        print("=" * 70)
        print("All examples completed!")
        print("=" * 70)

        # Ask if user wants to clean up
        response = input("\nDo you want to clean up the session data? (y/n): ")
        if response.lower() == "y":
            cleanup_sessions()

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
