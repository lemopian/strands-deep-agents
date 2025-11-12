"""
Factory functions for creating DeepAgents using Strands SDK.

This module provides functions to create deep agents with planning, file operations,
and sub-agent delegation capabilities, adapted from the LangChain DeepAgents pattern
to work with the Strands Agents SDK architecture.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from strands import Agent
from strands.models import Model
from strands.session.session_manager import SessionManager
from strands.tools.executors import SequentialToolExecutor
from strands_tools import editor, file_read, file_write

from strands_deep_agents.ai_models import get_default_model
from strands_deep_agents.prompts import get_deep_agent_prompt
from strands_deep_agents.sub_agents import create_async_task_tool, create_task_tool
from strands_deep_agents.tools.planning import write_todos
from strands_deep_agents.types import CustomSubAgent, SubAgent


def create_deep_agent(
    tools: Optional[Sequence[Union[Callable, dict[str, Any]]]] = None,
    instructions: str = "",
    model: Optional[str | Model] = None,
    subagents: Optional[List[Union[SubAgent, CustomSubAgent]]] = None,
    initial_state: Optional[Dict[str, Any]] = None,
    disable_parallel_tool_calling: bool = False,
    session_manager: Optional[SessionManager] = None,
    **kwargs,
) -> Agent:
    """
    Create a deep agent with planning, file operations, and sub-agent capabilities.

    This agent will by default have access to:
    - write_todos tool for task planning
    - File editing tools (file_read, file_write, editor from strands_tools)
    - A tool to call subagents

    Args:
        tools: The tools the agent should have access to
        instructions: Additional instructions for the agent (appended to base prompt)
        model: The model identifier to use (default: Claude Sonnet 4)
        subagents: List of specialized subagents, each with:
            - `name`: Unique identifier
            - `description`: Used by main agent to decide when to call
            - `prompt`: System prompt for the subagent
            - (optional) `tools`: Tools specific to this subagent
            - (optional) `model`: Model override for this subagent
        initial_state: Initial agent state (todos, etc.)
        disable_parallel_tool_calling: If True, disables parallel execution of tools and
            sub-agents, forcing sequential execution. Useful for debugging or when tools
            have dependencies.
        session_manager: Optional session manager for persisting agent state and conversation
            history across sessions. Use FileSessionManager for local persistence or
            S3SessionManager for cloud-based persistence. If provided, the agent will
            automatically restore state from previous sessions and persist changes.
        **kwargs: Additional arguments passed to Agent constructor

    Returns:
        Configured Strands Agent with DeepAgent capabilities

    Example:
        ```python
        from strands_deep_agents import create_deep_agent

        # Create a simple deep agent
        agent = create_deep_agent(
            instructions="You are a helpful coding assistant."
        )

        # Create with custom sub-agents
        code_reviewer = {
            "name": "code_reviewer",
            "description": "Reviews code for quality and best practices",
            "prompt": "You are an expert code reviewer."
        }

        agent = create_deep_agent(
            instructions="You are a senior developer.",
            subagents=[code_reviewer]
        )

        # Create with sequential tool execution
        agent = create_deep_agent(
            instructions="You are a helpful assistant.",
            disable_parallel_tool_calling=True
        )

        # Create with session persistence (file-based)
        from strands.session.file_session_manager import FileSessionManager

        session_manager = FileSessionManager(
            session_id="user-123",
            storage_dir="./sessions"
        )
        agent = create_deep_agent(
            instructions="You are a helpful assistant.",
            session_manager=session_manager
        )

        # Use the agent
        result = agent("Help me build a calculator module")
        ```
    """
    # Set default model if not provided
    if model is None:
        model = get_default_model()

    # Initialize with user-provided tools
    all_tools = list(tools) if tools else []

    all_tools.extend([file_read, file_write, editor])

    # Add planning tool
    all_tools.append(write_todos)

    # Prepare list of all subagents for TASK_TOOL_DESCRIPTION formatting
    all_subagents = list(subagents) if subagents else []

    # Create a single task tool that dispatches to all subagents
    task_tool = create_task_tool(
        default_tools=all_tools,
        subagents=all_subagents,
        default_model=model,
        disable_parallel_tool_calling=disable_parallel_tool_calling,
    )

    # Add the task tool to all_tools
    all_tools.append(task_tool)

    # Extract only the parameters that get_deep_agent_prompt accepts
    prompt_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in {"enable_planning", "enable_file_system", "has_sub_agents"}
    }

    # Auto-detect if sub-agents are present
    if all_subagents and "has_sub_agents" not in prompt_kwargs:
        prompt_kwargs["has_sub_agents"] = True

    system_prompt = get_deep_agent_prompt(user_instructions=instructions, **prompt_kwargs)

    # Prepare initial state
    agent_state = initial_state or {}
    if "todos" not in agent_state:
        agent_state["todos"] = []

    # Prepare agent kwargs
    agent_kwargs = {
        "system_prompt": system_prompt,
        "tools": all_tools,
        "model": model,
        "state": agent_state,
        **kwargs,
    }

    # Add session manager if provided
    if session_manager is not None:
        agent_kwargs["session_manager"] = session_manager

    # Use SequentialToolExecutor if parallel execution is disabled
    if disable_parallel_tool_calling:
        agent_kwargs["tool_executor"] = SequentialToolExecutor()

    # Create and return the agent
    agent = Agent(**agent_kwargs)

    return agent


async def async_create_deep_agent(
    tools: Optional[Sequence[Union[Callable, dict[str, Any]]]] = None,
    instructions: str = "",
    model: Optional[str | Model] = None,
    subagents: Optional[List[Union[SubAgent, CustomSubAgent]]] = None,
    initial_state: Optional[Dict[str, Any]] = None,
    disable_parallel_tool_calling: bool = False,
    session_manager: Optional[SessionManager] = None,
    **kwargs,
) -> Agent:
    """
    Create an async deep agent with planning, file operations, and sub-agent capabilities.

    This is the async version of create_deep_agent. The agent will use async sub-agent
    tools for parallel execution.

    Args:
        tools: The tools the agent should have access to
        instructions: Additional instructions for the agent (appended to base prompt)
        model: The model identifier to use (default: Claude Sonnet 4)
        subagents: List of specialized subagents
        initial_state: Initial agent state (todos, etc.)
        disable_parallel_tool_calling: If True, disables parallel execution of tools and
            sub-agents, forcing sequential execution. Useful for debugging or when tools
            have dependencies.
        session_manager: Optional session manager for persisting agent state and conversation
            history across sessions. Use FileSessionManager for local persistence or
            S3SessionManager for cloud-based persistence. If provided, the agent will
            automatically restore state from previous sessions and persist changes.
        **kwargs: Additional arguments passed to Agent constructor

    Returns:
        Configured async Strands Agent with DeepAgent capabilities

    Example:
        ```python
        from strands_deep_agents import async_create_deep_agent
        from strands.session.file_session_manager import FileSessionManager
        import asyncio

        async def main():
            # Create with session persistence
            session_manager = FileSessionManager(
                session_id="async-user-123",
                storage_dir="./sessions"
            )
            agent = await async_create_deep_agent(
                instructions="You are a helpful assistant.",
                session_manager=session_manager
            )
            result = await agent.invoke_async("Help me with a task")
            print(result)

        asyncio.run(main())
        ```
    """
    # Set default model if not provided
    if model is None:
        model = get_default_model()

    # Initialize with user-provided tools
    all_tools = list(tools) if tools else []

    # Add file system tools (using strands_tools)
    all_tools.extend([file_read, file_write, editor])

    # Add planning tool
    all_tools.append(write_todos)

    # Prepare list of all subagents for TASK_TOOL_DESCRIPTION formatting
    all_subagents = list(subagents) if subagents else []

    # Create a single async task tool that dispatches to all subagents
    task_tool = await create_async_task_tool(
        default_tools=all_tools,
        subagents=all_subagents,
        default_model=model,
        disable_parallel_tool_calling=disable_parallel_tool_calling,
    )

    # Add the task tool to all_tools
    all_tools.append(task_tool)

    # Extract only the parameters that get_deep_agent_prompt accepts
    prompt_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in {"enable_planning", "enable_file_system", "has_sub_agents"}
    }

    # Auto-detect if sub-agents are present
    if all_subagents and "has_sub_agents" not in prompt_kwargs:
        prompt_kwargs["has_sub_agents"] = True

    system_prompt = get_deep_agent_prompt(user_instructions=instructions, **prompt_kwargs)

    # Prepare initial state
    agent_state = initial_state or {}
    if "todos" not in agent_state:
        agent_state["todos"] = []

    # Prepare agent kwargs
    agent_kwargs = {
        "system_prompt": system_prompt,
        "tools": all_tools,
        "model": model,
        "state": agent_state,
        **kwargs,
    }

    # Add session manager if provided
    if session_manager is not None:
        agent_kwargs["session_manager"] = session_manager

    # Use SequentialToolExecutor if parallel execution is disabled
    if disable_parallel_tool_calling:
        agent_kwargs["tool_executor"] = SequentialToolExecutor()

    # Create and return the agent
    agent = Agent(**agent_kwargs)

    return agent
