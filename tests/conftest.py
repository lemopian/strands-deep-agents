"""
Pytest configuration and fixtures for Strands DeepAgents tests.
"""

import os

import pytest
from strands import Agent, tool


@pytest.fixture(autouse=True)
def bypass_tool_consent():
    """Automatically bypass tool consent for all tests."""
    os.environ["BYPASS_TOOL_CONSENT"] = "true"
    yield
    # Cleanup
    if "BYPASS_TOOL_CONSENT" in os.environ:
        del os.environ["BYPASS_TOOL_CONSENT"]


@pytest.fixture
def sample_todos():
    """Provide sample TODO items for testing."""
    return [
        {"id": "1", "content": "Task 1", "status": "pending"},
        {"id": "2", "content": "Task 2", "status": "in_progress"},
        {"id": "3", "content": "Task 3", "status": "completed"},
    ]


@pytest.fixture
def default_model():
    """Provide default model identifier."""
    return "global.anthropic.claude-sonnet-4-5-20250929-v1:0"


@pytest.fixture
def sample_tool():
    """Provide a sample tool for testing."""

    @tool
    def test_tool(value: str) -> str:
        """A test tool that echoes input."""
        return f"Echo: {value}"

    return test_tool


@pytest.fixture
def sample_sub_agent():
    """Provide a sample sub-agent configuration."""
    return {
        "name": "test_agent",
        "description": "A test sub-agent for testing purposes",
        "prompt": "You are a test agent. Always respond helpfully.",
    }


@pytest.fixture
def agent_with_planning():
    """Provide an agent with planning tools."""
    from strands_deep_agents.tools import write_todos

    return Agent(tools=[write_todos])


@pytest.fixture
def multiple_todos():
    """Provide multiple TODO items with various statuses."""
    return [
        {"id": "1", "content": "Design database schema", "status": "completed"},
        {"id": "2", "content": "Implement API endpoints", "status": "in_progress"},
        {"id": "3", "content": "Write unit tests", "status": "pending"},
        {"id": "4", "content": "Deploy to staging", "status": "pending"},
        {"id": "5", "content": "Code review", "status": "in_progress"},
    ]


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio to only use asyncio backend."""
    return "asyncio"
