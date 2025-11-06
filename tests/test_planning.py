"""
Tests for planning tools (write_todos, get_todos).
"""

import pytest
from strands import Agent
from strands_deepagents.tools import write_todos


class TestPlanningTools:
    """Test suite for planning tools."""

    def test_write_todos_creates_new_list(self):
        """Test creating a new TODO list."""
        agent = Agent(tools=[write_todos, get_todos])

        result = agent.tool.write_todos(
            todos=[
                {"id": "1", "content": "Task 1", "status": "pending"},
                {"id": "2", "content": "Task 2", "status": "in_progress"},
            ],
            merge=False,
        )

        assert "TODO list updated" in result
        assert "Total: 2 tasks" in result

        # Verify state
        todos = agent.state.get("todos")
        assert len(todos) == 2
        assert todos[0]["id"] == "1"
        assert todos[0]["content"] == "Task 1"
        assert todos[0]["status"] == "pending"

    def test_write_todos_merge(self):
        """Test merging TODOs with existing list."""
        agent = Agent(tools=[write_todos, get_todos])

        # Create initial todos
        agent.state.set("todos", [{"id": "1", "content": "Original Task", "status": "completed"}])

        # Merge new todos
        result = agent.tool.write_todos(
            todos=[
                {"id": "1", "content": "Updated Task", "status": "completed"},
                {"id": "2", "content": "New Task", "status": "pending"},
            ],
            merge=True,
        )

        todos = agent.state.get("todos")
        assert len(todos) == 2
        assert todos[0]["content"] == "Updated Task"
        assert todos[1]["content"] == "New Task"

    def test_write_todos_validation(self):
        """Test TODO validation."""
        agent = Agent(tools=[write_todos])

        # Missing required field
        result = agent.tool.write_todos(
            todos=[{"id": "1", "content": "Task"}], merge=False  # Missing status
        )
        assert "Error" in result
        assert "status" in result

    def test_write_todos_invalid_status(self):
        """Test invalid status handling."""
        agent = Agent(tools=[write_todos])

        result = agent.tool.write_todos(
            todos=[{"id": "1", "content": "Task", "status": "invalid"}], merge=False
        )
        assert "Error" in result
        assert "Invalid status" in result

    def test_get_todos_empty(self):
        """Test getting TODOs when none exist."""
        agent = Agent(tools=[get_todos])

        result = agent.tool.get_todos()
        assert "No TODOs" in result

    def test_get_todos_with_items(self):
        """Test getting TODOs with items."""
        agent = Agent(tools=[get_todos])

        agent.state.set(
            "todos",
            [
                {"id": "1", "content": "Task 1", "status": "pending"},
                {"id": "2", "content": "Task 2", "status": "completed"},
            ],
        )

        result = agent.tool.get_todos()
        assert "Current TODO List" in result
        assert "Task 1" in result
        assert "Task 2" in result
        assert "pending" in result
        assert "completed" in result

    def test_status_counts(self):
        """Test status counting in write_todos."""
        agent = Agent(tools=[write_todos])

        result = agent.tool.write_todos(
            todos=[
                {"id": "1", "content": "T1", "status": "pending"},
                {"id": "2", "content": "T2", "status": "pending"},
                {"id": "3", "content": "T3", "status": "in_progress"},
                {"id": "4", "content": "T4", "status": "completed"},
            ],
            merge=False,
        )

        assert "Pending: 2" in result
        assert "In Progress: 1" in result
        assert "Completed: 1" in result
