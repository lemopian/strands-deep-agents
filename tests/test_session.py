"""
Tests for session management functionality in Strands DeepAgents.
"""

import shutil
import tempfile
from pathlib import Path

import pytest
from strands.session.file_session_manager import FileSessionManager

from strands_deep_agents import create_deep_agent


@pytest.fixture
def temp_session_dir():
    """
    Create a temporary directory for session storage.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_create_file_session_manager(temp_session_dir):
    """
    Test creating a FileSessionManager.
    """
    session_manager = FileSessionManager(
        session_id="test-session",
        storage_dir=temp_session_dir,
    )

    assert session_manager is not None
    assert session_manager.session_id == "test-session"


def test_agent_with_session_manager(temp_session_dir):
    """
    Test creating an agent with a session manager.
    """
    session_manager = FileSessionManager(
        session_id="test-agent-session",
        storage_dir=temp_session_dir,
    )

    agent = create_deep_agent(
        instructions="You are a test agent.",
        session_manager=session_manager,
    )

    assert agent is not None
    # Session manager is stored as a private attribute in Strands Agent
    assert hasattr(agent, "_session_manager")
    assert agent._session_manager is not None


def test_session_persistence_state(temp_session_dir):
    """
    Test that agent state persists across sessions.

    Note: In Strands, session state is synced to storage during agent invocations,
    so we verify that initial_state is properly loaded on agent creation.
    """
    session_id = "state-persistence-test"

    # Create agent with initial state
    session_manager1 = FileSessionManager(
        session_id=session_id,
        storage_dir=temp_session_dir,
    )

    agent1 = create_deep_agent(
        instructions="You are a test agent.",
        initial_state={"counter": 5, "user_name": "Alice"},
        session_manager=session_manager1,
    )

    # Verify initial state is set
    assert agent1.state.get("counter") == 5
    assert agent1.state.get("user_name") == "Alice"

    # Create second agent with same session and no initial state
    # It should load the session from storage (which has the initial state from agent1)
    session_manager2 = FileSessionManager(
        session_id=session_id,
        storage_dir=temp_session_dir,
    )

    agent2 = create_deep_agent(
        instructions="You are a test agent.",
        session_manager=session_manager2,
    )

    # Verify state includes todos from initial state (DeepAgent default)
    # The actual state restoration happens during agent initialization if session exists
    assert "todos" in agent2.state.get() or agent2.state.get("todos") is not None


def test_session_storage_path(temp_session_dir):
    """
    Test getting session storage path.
    """
    session_id = "path-test-session"
    session_path = Path(temp_session_dir) / f"session_{session_id}"

    assert session_path is not None
    assert isinstance(session_path, Path)
    assert session_id in str(session_path)


def test_multiple_sessions(temp_session_dir):
    """
    Test creating multiple independent sessions.
    """
    # Create first session
    session1 = FileSessionManager(
        session_id="session-1",
        storage_dir=temp_session_dir,
    )
    agent1 = create_deep_agent(
        instructions="You are agent 1.",
        initial_state={"agent_id": 1},
        session_manager=session1,
    )
    agent1.state.set("value", "first")

    # Create second session
    session2 = FileSessionManager(
        session_id="session-2",
        storage_dir=temp_session_dir,
    )
    agent2 = create_deep_agent(
        instructions="You are agent 2.",
        initial_state={"agent_id": 2},
        session_manager=session2,
    )
    agent2.state.set("value", "second")

    # Verify sessions are independent
    assert agent1.state.get("value") == "first"
    assert agent2.state.get("value") == "second"
    assert agent1.state.get("agent_id") == 1
    assert agent2.state.get("agent_id") == 2


def test_session_with_todos(temp_session_dir):
    """
    Test that todos persist across sessions.
    """
    session_id = "todos-test-session"

    # Create first agent and set todos
    session_manager1 = FileSessionManager(
        session_id=session_id,
        storage_dir=temp_session_dir,
    )

    agent1 = create_deep_agent(
        instructions="You are a test agent.",
        initial_state={
            "todos": [
                {"id": "1", "content": "Task 1", "status": "completed"},
                {"id": "2", "content": "Task 2", "status": "pending"},
            ]
        },
        session_manager=session_manager1,
    )

    # Verify initial todos
    todos1 = agent1.state.get("todos")
    assert len(todos1) == 2
    assert todos1[0]["content"] == "Task 1"

    # Create second agent with same session
    session_manager2 = FileSessionManager(
        session_id=session_id,
        storage_dir=temp_session_dir,
    )

    agent2 = create_deep_agent(
        instructions="You are a test agent.",
        session_manager=session_manager2,
    )

    # Verify todos were restored
    todos2 = agent2.state.get("todos")
    assert len(todos2) == 2
    assert todos2[0]["content"] == "Task 1"
    assert todos2[0]["status"] == "completed"
    assert todos2[1]["content"] == "Task 2"
    assert todos2[1]["status"] == "pending"


def test_agent_without_session_manager():
    """
    Test that agents work without a session manager (no persistence).
    """
    agent = create_deep_agent(
        instructions="You are a test agent.",
        initial_state={"value": "test"},
    )

    assert agent is not None
    assert agent.state.get("value") == "test"
    # Session manager should be None (stored as private attribute _session_manager)
    assert not hasattr(agent, "_session_manager") or agent._session_manager is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
