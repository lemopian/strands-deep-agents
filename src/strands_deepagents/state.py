"""
State definitions for Strands DeepAgents.
"""

from typing import Annotated, Literal, NotRequired, TypedDict

from typing_extensions import TypedDict as TypedDictExt

TodoStatus = Literal["pending", "in_progress", "completed"]


class Todo(TypedDict):
    """
    Todo item to track task progress.

    Attributes:
        content: Description of the todo item
        status: Current status of the todo
            - pending: Task not yet started (default state for future tasks)
            - in_progress: Currently being worked on (agent should have at least
              one task in this state to show it is active)
            - completed: Task finished successfully with no unresolved issues or blockers

    Error/Blocker Handling:
        - If you encounter errors or blockers, keep the task as in_progress
        - When blocked, create a new task describing what needs to be resolved
    """

    id: str
    content: str
    status: TodoStatus


def file_reducer(left: dict | None, right: dict | None) -> dict | None:
    """
    Reducer function for merging file dictionaries.

    Args:
        left: Current state value
        right: New state value to merge

    Returns:
        Merged dictionary or None
    """
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class DeepAgentState(TypedDictExt):
    """
    Combined state for DeepAgent with todos and files.

    Attributes:
        todos: List of todo items for tracking progress
        files: Dictionary mapping file paths to content (reduced with file_reducer)
    """

    todos: NotRequired[list[Todo]]
    files: Annotated[
        NotRequired[dict[str, str]], file_reducer
    ]  # TODO: make sure strands-tools file tools are used to update this
