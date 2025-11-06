"""
Pytest configuration and fixtures for Strands DeepAgents tests.
"""

import pytest
import os


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
