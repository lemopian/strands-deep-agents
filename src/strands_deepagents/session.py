"""
Session management utilities for DeepAgents.

This module provides helper functions and utilities for managing agent sessions,
enabling state persistence and recovery across agent invocations.
"""

from typing import Optional
from pathlib import Path
from strands.session.file_session_manager import FileSessionManager
from strands.session.session_manager import SessionManager


def create_file_session_manager(
    session_id: str,
    storage_dir: Optional[str] = None,
) -> FileSessionManager:
    """
    Create a FileSessionManager for local session persistence.

    This session manager stores agent state and conversation history in the local
    filesystem, ensuring persistence even in case of application failure or restart.

    Args:
        session_id: Unique identifier for the session. Use this to restore
            previous sessions or create new ones.
        storage_dir: Directory path for storing session data. If None, uses
            a default temporary directory. It's recommended to specify a
            directory for production use.

    Returns:
        Configured FileSessionManager instance

    Example:
        ```python
        from strands_deepagents import create_deep_agent
        from strands_deepagents.session import create_file_session_manager

        # Create session manager
        session_manager = create_file_session_manager(
            session_id="user-123",
            storage_dir="./agent_sessions"
        )

        # Create agent with session persistence
        agent = create_deep_agent(
            instructions="You are a helpful assistant.",
            session_manager=session_manager
        )

        # First interaction
        agent("Hello, my name is John")

        # Later, create a new agent instance with the same session_id
        # The agent will automatically restore the previous conversation
        agent2 = create_deep_agent(
            instructions="You are a helpful assistant.",
            session_manager=create_file_session_manager(
                session_id="user-123",
                storage_dir="./agent_sessions"
            )
        )

        # The agent remembers the previous conversation
        agent2("What's my name?")  # Will respond with "John"
        ```
    """
    return FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )


def create_s3_session_manager(
    session_id: str,
    bucket: str,
    prefix: Optional[str] = None,
    region_name: Optional[str] = None,
) -> SessionManager:
    """
    Create an S3SessionManager for cloud-based session persistence.

    This session manager stores agent state and conversation history in Amazon S3,
    enabling distributed deployments and cross-instance persistence.

    Args:
        session_id: Unique identifier for the session
        bucket: Name of the S3 bucket for storing session data
        prefix: Optional key prefix for organizing sessions in the bucket
        region_name: AWS region name. If not specified, uses the default
            region from AWS credentials

    Returns:
        Configured S3SessionManager instance

    Example:
        ```python
        from strands_deepagents import create_deep_agent
        from strands_deepagents.session import create_s3_session_manager

        # Create S3-backed session manager
        session_manager = create_s3_session_manager(
            session_id="user-456",
            bucket="my-agent-sessions",
            prefix="production/",
            region_name="us-west-2"
        )

        # Create agent with S3 persistence
        agent = create_deep_agent(
            instructions="You are a helpful assistant.",
            session_manager=session_manager
        )

        # Agent state and conversation are persisted to S3
        agent("Process this important task")
        ```

    Note:
        Requires appropriate AWS credentials and S3 permissions:
        - s3:PutObject - To create and update session data
        - s3:GetObject - To retrieve session data
        - s3:DeleteObject - To delete session data
        - s3:ListBucket - To list objects in the bucket
    """
    from strands.session.s3_session_manager import S3SessionManager

    return S3SessionManager(
        session_id=session_id,
        bucket=bucket,
        prefix=prefix,
        region_name=region_name,
    )


def get_session_storage_path(
    session_id: str,
    storage_dir: Optional[str] = None,
) -> Path:
    """
    Get the filesystem path where a session is stored.

    Useful for debugging, backup, or manual session management.

    Args:
        session_id: The session identifier
        storage_dir: The storage directory used for the session manager.
            If None, returns the default temporary directory path.

    Returns:
        Path object pointing to the session directory

    Example:
        ```python
        from strands_deepagents.session import get_session_storage_path
        import shutil

        # Get session path
        session_path = get_session_storage_path(
            session_id="user-123",
            storage_dir="./agent_sessions"
        )

        # Backup the session
        if session_path.exists():
            shutil.copytree(session_path, f"./backups/{session_path.name}")

        # Check session size
        total_size = sum(
            f.stat().st_size for f in session_path.rglob('*') if f.is_file()
        )
        print(f"Session size: {total_size / 1024:.2f} KB")
        ```
    """
    if storage_dir is None:
        # Use the same default as FileSessionManager
        from tempfile import gettempdir

        storage_dir = Path(gettempdir()) / "strands_sessions"
    else:
        storage_dir = Path(storage_dir)

    return storage_dir / f"session_{session_id}"
