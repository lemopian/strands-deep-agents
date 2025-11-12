"""
Sub-agent implementation using the Agents-as-Tools pattern from Strands.
"""

import logging
from typing import Any, Dict, List, Union

from strands import Agent, tool
from strands.tools.executors import SequentialToolExecutor

from strands_deep_agents.prompts import BASE_AGENT_PROMPT, TASK_TOOL_DESCRIPTION
from strands_deep_agents.types import CustomSubAgent, SubAgent

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)


def _get_subagents_description(subagents: List[Union[SubAgent, CustomSubAgent]]) -> str:
    """
    Generate formatted description of available subagents.

    Args:
        subagents: List of subagent configurations

    Returns:
        Formatted string listing subagents
    """
    if not subagents:
        return ""
    return "\n".join([f"- {agent['name']}: {agent['description']}" for agent in subagents])


def _build_subagents_configs(
    default_tools: List[Any],
    subagents: List[Union[SubAgent, CustomSubAgent]],
    default_model: str,
    disable_parallel_tool_calling: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Build a dictionary of agent configurations (not instances) keyed by their names.

    Agent instances are created fresh for each invocation to avoid state accumulation.

    Args:
        default_tools: Default tools to include if sub_agent doesn't specify any
        subagents: List of all subagent configurations
        default_model: Default model if sub_agent doesn't specify one
        disable_parallel_tool_calling: If True, sub-agents will use sequential tool execution

    Returns:
        Dictionary mapping agent names to configuration dicts
    """
    configs = {}

    # Store configurations for subagents
    for sub_agent_config in subagents:
        configs[sub_agent_config["name"]] = {
            "system_prompt": sub_agent_config.get("prompt", ""),
            "tools": sub_agent_config.get("tools", default_tools),
            "model": sub_agent_config.get("model", default_model),
            "disable_parallel_tool_calling": sub_agent_config.get(
                "disable_parallel_tool_calling", disable_parallel_tool_calling
            ),
        }

    return configs


def create_task_tool(
    default_tools: List[Any],
    subagents: List[Union[SubAgent, CustomSubAgent]],
    default_model: str,
    disable_parallel_tool_calling: bool = False,
) -> Any:
    """
    Create a single task tool that dispatches to multiple subagents.

    This implements the "Agents as Tools" pattern where a single tool
    can invoke different specialized agents based on the subagent_type parameter.

    Args:
        default_tools: Default tools to include if sub_agent doesn't specify any
        subagents: List of all subagent configurations
        default_model: Default model if sub_agent doesn't specify one
        disable_parallel_tool_calling: If True, sub-agents will use sequential tool execution

    Returns:
        A tool function that can execute any of the configured subagents
    """
    # Build the dictionary of agent configurations
    subagents_configs = _build_subagents_configs(
        default_tools, subagents, default_model, disable_parallel_tool_calling
    )

    # Format the tool description with available subagents
    sub_agents_desc = _get_subagents_description(subagents)
    tool_description = TASK_TOOL_DESCRIPTION.format(sub_agents=sub_agents_desc)

    @tool(description=tool_description)
    def task(description: str, subagent_type: str) -> str:
        """
        Launch an ephemeral subagent to handle a task.

        Args:
            description: The task or question for the specialized agent
            subagent_type: The type of agent to use (e.g. custom agent names)

        Returns:
            The result from the subagent
        """
        logger.info(f"🚀 Launching subagent: type='{subagent_type}'")
        logger.debug(
            f"   Task description: {description[:100]}{'...' if len(description) > 100 else ''}"
        )

        if subagent_type not in subagents_configs:
            allowed_types = [f"`{k}`" for k in subagents_configs.keys()]
            error_msg = f"Error: invoked agent of type {subagent_type}, the only allowed types are {allowed_types}"
            logger.error(f"❌ {error_msg}")
            return error_msg

        try:
            config = subagents_configs[subagent_type]
            logger.info(f"⚙️  Executing subagent '{subagent_type}'...")

            # Create a fresh Agent instance for each invocation
            # This prevents state accumulation across multiple calls
            agent_kwargs = {
                "system_prompt": config["system_prompt"],
                "tools": config["tools"],
                "model": config["model"],
            }

            # Use SequentialToolExecutor if parallel execution is disabled
            if config.get("disable_parallel_tool_calling", False):
                agent_kwargs["tool_executor"] = SequentialToolExecutor()

            sub_agent = Agent(**agent_kwargs)

            response = sub_agent(description)
            logger.info(f"✅ Subagent '{subagent_type}' completed successfully")
            logger.debug(f"   Response length: {len(str(response))} characters")
            return str(response)
        except Exception as e:
            error_msg = f"Error in {subagent_type}: {str(e)}"
            logger.error(f"❌ Subagent '{subagent_type}' failed: {str(e)}")
            return error_msg

    return task


async def create_async_task_tool(
    default_tools: List[Any],
    subagents: List[Union[SubAgent, CustomSubAgent]],
    default_model: str,
    disable_parallel_tool_calling: bool = False,
) -> Any:
    """
    Create a single async task tool that dispatches to multiple subagents.

    This implements the "Agents as Tools" pattern for async execution.

    Args:
        default_tools: Default tools to include if sub_agent doesn't specify any
        subagents: List of all subagent configurations
        default_model: Default model if sub_agent doesn't specify one
        disable_parallel_tool_calling: If True, sub-agents will use sequential tool execution

    Returns:
        An async tool function that can execute any of the configured subagents
    """
    # Build the dictionary of agent configurations
    subagents_configs = _build_subagents_configs(
        default_tools, subagents, default_model, disable_parallel_tool_calling
    )

    # Format the tool description with available subagents
    sub_agents_desc = _get_subagents_description(subagents)
    tool_description = TASK_TOOL_DESCRIPTION.format(sub_agents=sub_agents_desc)

    @tool(description=tool_description)
    async def task(description: str, subagent_type: str) -> str:
        """
        Launch an ephemeral subagent to handle a task.

        Args:
            description: The task or question for the specialized agent
            subagent_type: The type of agent to use (e.g., 'general-purpose', or custom agent names)

        Returns:
            The result from the subagent
        """
        logger.info(f"🚀 Launching async subagent: type='{subagent_type}'")
        logger.debug(
            f"   Task description: {description[:100]}{'...' if len(description) > 100 else ''}"
        )

        if subagent_type not in subagents_configs:
            allowed_types = [f"`{k}`" for k in subagents_configs.keys()]
            error_msg = f"Error: invoked agent of type {subagent_type}, the only allowed types are {allowed_types}"
            logger.error(f"❌ {error_msg}")
            return error_msg

        try:
            config = subagents_configs[subagent_type]
            logger.info(f"⚙️  Executing async subagent '{subagent_type}'...")

            # Create a fresh Agent instance for each invocation
            # This prevents state accumulation across multiple calls
            agent_kwargs = {
                "system_prompt": config["system_prompt"],
                "tools": config["tools"],
                "model": config["model"],
            }

            # Use SequentialToolExecutor if parallel execution is disabled
            if config.get("disable_parallel_tool_calling", False):
                agent_kwargs["tool_executor"] = SequentialToolExecutor()

            sub_agent = Agent(**agent_kwargs)

            response = await sub_agent.invoke_async(description)
            logger.info(f"✅ Async subagent '{subagent_type}' completed successfully")
            logger.debug(f"   Response length: {len(str(response))} characters")
            return str(response)
        except Exception as e:
            error_msg = f"Error in {subagent_type}: {str(e)}"
            logger.error(f"❌ Async subagent '{subagent_type}' failed: {str(e)}")
            return error_msg

    return task


def create_general_purpose_sub_agent(
    main_instructions: str, all_tools: List[Any], model: str
) -> SubAgent:
    """
    Create the default 'general_purpose' sub-agent that mirrors the main agent.

    This sub-agent has the same tools and instructions as the main agent and is
    useful for context quarantine - handling subtasks without polluting the main
    agent's context.

    Args:
        main_instructions: The main agent's system prompt
        all_tools: All tools available to the main agent
        model: Model identifier to use

    Returns:
        A SubAgent configuration for the general purpose agent
    """

    return {
        "name": "general-purpose",
        "description": (
            "General-purpose agent for researching complex questions, searching for files and content, "
            "and executing multi-step tasks. When you are searching for a keyword or file and are not "
            "confident that you will find the right match in the first few tries use this agent to perform "
            "the search for you. This agent has access to all tools as the main agent."
        ),
        "prompt": (
            main_instructions + "\n\n" + BASE_AGENT_PROMPT
            if main_instructions
            else BASE_AGENT_PROMPT
        ),
        "tools": all_tools,
        "model": model,
    }
