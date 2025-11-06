"""
State definitions for Strands DeepAgents.
"""

from typing import NotRequired, Literal, Annotated, TypedDict
from typing_extensions import TypedDict as TypedDictExt
from pydantic import BaseModel, Field


class Todo(TypedDict):
    """
    Todo item to track task progress.

    Attributes:
        content: Description of the todo item
        status: Current status of the todo
    """

    id: str
    content: str
    status: Literal["pending", "in_progress", "completed"]


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
    files: Annotated[NotRequired[dict[str, str]], file_reducer]


class PlanningState(TypedDictExt):
    """
    State for planning with todo tracking.

    Attributes:
        todos: List of todo items for tracking progress
    """

    todos: NotRequired[list[Todo]]
