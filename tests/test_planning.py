"""
Tests for planning tools (write_todos).
"""

import pytest
from strands import ToolContext

from strands_deep_agents.tools import TodoItem, write_todos


class TestPlanningTools:
    """Test suite for planning tools."""

    def test_write_todos_creates_new_list(self, agent_with_planning):
        """Test creating a new TODO list."""
        tool_use = {"toolUseId": "test-1", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(
            todos=[
                TodoItem(id="1", content="Task 1", status="pending"),
                TodoItem(id="2", content="Task 2", status="in_progress"),
            ],
            tool_context=tool_context,
            merge=False,
        )

        assert "TODO list updated" in result
        assert "Total: 2 tasks" in result

        # Verify state
        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 2
        assert todos[0]["id"] == "1"
        assert todos[0]["content"] == "Task 1"
        assert todos[0]["status"] == "pending"

    def test_write_todos_merge(self, agent_with_planning):
        """Test merging TODOs with existing list."""
        # Create initial todos
        agent_with_planning.state.set(
            "todos", [{"id": "1", "content": "Original Task", "status": "completed"}]
        )

        tool_use = {"toolUseId": "test-2", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(
            todos=[
                TodoItem(id="1", content="Updated Task", status="completed"),
                TodoItem(id="2", content="New Task", status="pending"),
            ],
            tool_context=tool_context,
            merge=True,
        )

        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 2
        assert todos[0]["content"] == "Updated Task"
        assert todos[1]["content"] == "New Task"

    def test_status_counts(self, agent_with_planning):
        """Test status counting in write_todos."""
        tool_use = {"toolUseId": "test-3", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(
            todos=[
                TodoItem(id="1", content="T1", status="pending"),
                TodoItem(id="2", content="T2", status="pending"),
                TodoItem(id="3", content="T3", status="in_progress"),
                TodoItem(id="4", content="T4", status="completed"),
            ],
            tool_context=tool_context,
            merge=False,
        )

        assert "Pending: 2" in result
        assert "In Progress: 1" in result
        assert "Completed: 1" in result

    def test_write_todos_with_fixture(self, agent_with_planning, sample_todos):
        """Test write_todos using fixtures."""
        tool_use = {"toolUseId": "test-4", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        # Convert to TodoItem objects
        todo_items = [TodoItem(**t) for t in sample_todos]

        result = write_todos(todos=todo_items, tool_context=tool_context, merge=False)

        assert "TODO list updated" in result
        assert "Total: 3 tasks" in result

        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 3

    def test_merge_updates_existing_keeps_new(self, agent_with_planning):
        """Test that merge properly updates existing and adds new TODOs."""
        initial = [
            {"id": "1", "content": "Original 1", "status": "pending"},
            {"id": "2", "content": "Original 2", "status": "completed"},
        ]
        agent_with_planning.state.set("todos", initial)

        tool_use = {"toolUseId": "test-5", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        updates = [
            TodoItem(id="2", content="Updated 2", status="completed"),
            TodoItem(id="3", content="New 3", status="pending"),
        ]

        write_todos(todos=updates, tool_context=tool_context, merge=True)

        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 3
        assert todos[0]["content"] == "Original 1"  # Unchanged
        assert todos[1]["content"] == "Updated 2"  # Updated
        assert todos[2]["content"] == "New 3"  # New

    def test_empty_todos_list(self, agent_with_planning):
        """Test handling of empty TODO list."""
        tool_use = {"toolUseId": "test-6", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(todos=[], tool_context=tool_context, merge=False)

        assert "TODO list updated" in result
        todos = agent_with_planning.state.get("todos")
        assert len(todos) == 0

    def test_large_todo_list(self, agent_with_planning):
        """Test handling of large TODO list."""
        large_list = [
            TodoItem(id=str(i), content=f"Task {i}", status="pending") for i in range(100)
        ]

        tool_use = {"toolUseId": "test-7", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(todos=large_list, tool_context=tool_context, merge=False)

        assert "Total: 100 tasks" in result
        stored_todos = agent_with_planning.state.get("todos")
        assert len(stored_todos) == 100

    def test_unicode_in_todos(self, agent_with_planning):
        """Test handling of unicode characters in TODO content."""
        todos = [
            TodoItem(id="1", content="测试任务", status="pending"),
            TodoItem(id="2", content="Tâche de test 🚀", status="in_progress"),
            TodoItem(id="3", content="Задача тестирования", status="completed"),
        ]

        tool_use = {"toolUseId": "test-8", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        result = write_todos(todos=todos, tool_context=tool_context, merge=False)

        assert "TODO list updated" in result
        stored_todos = agent_with_planning.state.get("todos")
        assert stored_todos[0]["content"] == "测试任务"
        assert stored_todos[1]["content"] == "Tâche de test 🚀"


class TestPlanningIntegration:
    """Integration tests for planning tools."""

    def test_workflow_create_update_complete(self, agent_with_planning):
        """Test a complete workflow of creating, updating, and completing TODOs."""
        tool_use = {"toolUseId": "test-9", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        # Create initial TODOs
        initial = [
            TodoItem(id="1", content="Start project", status="pending"),
            TodoItem(id="2", content="Write code", status="pending"),
        ]
        write_todos(todos=initial, tool_context=tool_context, merge=False)

        # Update first to in_progress
        update1 = [TodoItem(id="1", content="Start project", status="in_progress")]
        write_todos(todos=update1, tool_context=tool_context, merge=True)

        # Complete first and start second
        update2 = [
            TodoItem(id="1", content="Start project", status="completed"),
            TodoItem(id="2", content="Write code", status="in_progress"),
        ]
        write_todos(todos=update2, tool_context=tool_context, merge=True)

        # Check final state
        todos = agent_with_planning.state.get("todos")
        assert todos[0]["status"] == "completed"
        assert todos[1]["status"] == "in_progress"

    def test_todos_state_persistence(self, agent_with_planning):
        """Test that TODO state persists across operations."""
        tool_use = {"toolUseId": "test-10", "name": "write_todos", "input": {}}
        tool_context = ToolContext(
            tool_use=tool_use, agent=agent_with_planning, invocation_state={}
        )

        # Create todos
        todos1 = [TodoItem(id="1", content="Task 1", status="pending")]
        write_todos(todos=todos1, tool_context=tool_context, merge=False)

        # Get state
        state1 = agent_with_planning.state.get("todos")
        assert len(state1) == 1

        # Add more todos
        todos2 = [TodoItem(id="2", content="Task 2", status="pending")]
        write_todos(todos=todos2, tool_context=tool_context, merge=True)

        # Check state again
        state2 = agent_with_planning.state.get("todos")
        assert len(state2) == 2


class TestTodoItemModel:
    """Test suite for TodoItem Pydantic model."""

    def test_todo_item_creation(self):
        """Test creating a TodoItem."""
        item = TodoItem(id="1", content="Test task", status="pending")

        assert item.id == "1"
        assert item.content == "Test task"
        assert item.status == "pending"

    def test_todo_item_dict_conversion(self):
        """Test converting TodoItem to dict."""
        item = TodoItem(id="1", content="Test task", status="completed")
        item_dict = item.model_dump()

        assert item_dict["id"] == "1"
        assert item_dict["content"] == "Test task"
        assert item_dict["status"] == "completed"

    def test_todo_item_all_statuses(self):
        """Test all valid status values."""
        statuses = ["pending", "in_progress", "completed"]

        for status in statuses:
            item = TodoItem(id="1", content="Test", status=status)
            assert item.status == status

    @pytest.mark.parametrize(
        "invalid_status",
        [
            "invalid",
            "PENDING",
            "done",
            "finished",
        ],
    )
    def test_todo_item_invalid_status(self, invalid_status):
        """Test that invalid status values are rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            TodoItem(id="1", content="Test", status=invalid_status)

    def test_todo_item_missing_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(Exception):  # Pydantic validation error
            TodoItem(id="1", content="Test")  # Missing status

        with pytest.raises(Exception):  # Pydantic validation error
            TodoItem(id="1", status="pending")  # Missing content

        with pytest.raises(Exception):  # Pydantic validation error
            TodoItem(content="Test", status="pending")  # Missing id
