"""
Planning tool for DeepAgents - enables agents to create and manage TODO lists.
"""

import logging
import traceback

from pydantic import BaseModel, Field
from strands import ToolContext, tool

from strands_deep_agents.prompts import WRITE_TODOS_TOOL_DESCRIPTION
from strands_deep_agents.state import TodoStatus

logger = logging.getLogger(__name__)


class TodoItem(BaseModel):
    """
    A single TODO item for tracking task progress.
    """

    id: str = Field(..., description="Unique identifier for the task")
    content: str = Field(..., description="Description of the task")
    status: TodoStatus = Field(..., description="Current status of the task")


@tool(context=True, description=WRITE_TODOS_TOOL_DESCRIPTION)
def write_todos(todos: list[TodoItem], tool_context: ToolContext, merge: bool = False) -> str:
    """
    Create or update a TODO list to track tasks and plan complex work.

    Use this tool to break down complex tasks into manageable steps. This helps
    maintain focus and track progress through multi-step workflows.

    Args:
        todos: List of TODO items with id, content, and status
        merge: If True, merge with existing todos (update by id).
            If False, replace all todos.

    Returns:
        Confirmation message with current TODO status

    Example:
        write_todos(
            todos=[
                TodoItem(id="1", content="Research the topic", status="completed"),
                TodoItem(id="2", content="Write outline", status="in_progress"),
                TodoItem(id="3", content="Draft content", status="pending")
            ],
            merge=False
        )
    """
    try:
        agent = tool_context.agent

        # Log tool invocation
        mode = "merge" if merge else "replace"
        logger.info(f"📝 write_todos called: mode={mode}, incoming_todos={len(todos)}")

        # Convert Pydantic models to dicts for storage
        # Handle both cases: when todos are already dicts or when they're Pydantic models
        todos_dicts = []
        for todo in todos:
            if isinstance(todo, dict):
                todos_dicts.append(todo)
                logger.debug(f"  → Todo already dict: {todo.get('id', 'unknown')}")
            else:
                todos_dicts.append(todo.model_dump())
                logger.debug(f"  → Converted Pydantic model to dict: {todo.id}")

        # Get existing todos
        existing_todos = agent.state.get("todos") or []
        logger.info(f"📋 Current state: {len(existing_todos)} existing todos")

        if merge and existing_todos:
            # Merge: update existing and add new
            logger.info("🔀 Merging todos with existing list")
            existing_dict = {t["id"]: t for t in existing_todos}
            updated_count = 0
            added_count = 0

            for todo_dict in todos_dicts:
                todo_id = todo_dict["id"]
                if todo_id in existing_dict:
                    logger.info(
                        f"  ✏️  Updated todo {todo_id}: '{todo_dict['content']}' → {todo_dict['status']}"
                    )
                    updated_count += 1
                else:
                    logger.info(
                        f"  ➕ Added new todo {todo_id}: '{todo_dict['content']}' → {todo_dict['status']}"
                    )
                    added_count += 1
                existing_dict[todo_id] = todo_dict

            updated_todos = list(existing_dict.values())
            logger.info(f"✅ Merge complete: {updated_count} updated, {added_count} added")
        else:
            # Replace all todos
            if existing_todos:
                logger.info(
                    f"🔄 Replacing all {len(existing_todos)} existing todos with {len(todos_dicts)} new todos"
                )
            else:
                logger.info(f"✨ Creating initial todo list with {len(todos_dicts)} todos")
            updated_todos = todos_dicts

            # Log each new todo
            for todo_dict in todos_dicts:
                logger.info(
                    f"  • {todo_dict['id']}: '{todo_dict['content']}' [{todo_dict['status']}]"
                )

        # Save to agent state using set method
        agent.state.set("todos", updated_todos)
        logger.debug("💾 Todos saved to agent state")

        # Generate summary
        status_counts = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
        }

        for todo in updated_todos:
            status = todo["status"]
            if status in status_counts:
                status_counts[status] += 1

        summary = f"TODO list updated. Total: {len(updated_todos)} tasks\n"
        summary += f"- Pending: {status_counts['pending']}\n"
        summary += f"- In Progress: {status_counts['in_progress']}\n"
        summary += f"- Completed: {status_counts['completed']}"

        logger.info(f"📊 Final summary: {status_counts}")
        print(summary)
        return summary

    except Exception as e:
        error_msg = f"Error in write_todos: {type(e).__name__}: {str(e)}"
        logger.error(f"❌ {error_msg}")

        logger.error(f"Traceback: {traceback.format_exc()}")
        return f"Error: {error_msg}"
