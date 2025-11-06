"""
Type definitions for Strands DeepAgents using TypedDict pattern.
"""

from typing import Any, NotRequired
from typing_extensions import TypedDict
from strands.models import Model
from strands import Agent


class SubAgent(TypedDict):
    """
    Configuration for a specialized sub-agent.

    This uses TypedDict to match the inspiration's pattern while being compatible
    with Strands Agent architecture.

    Attributes:
        name: Unique identifier for the sub-agent
        description: Description of sub-agent's purpose (shown to main agent)
        prompt: Detailed system prompt for the sub-agent
        tools: Optional list of tools available to the sub-agent
        model: Optional model identifier override for this sub-agent
    """

    name: str
    description: str
    prompt: str
    tools: NotRequired[list[Any]]
    model: NotRequired[str | Model]


class CustomSubAgent(TypedDict):
    """
    Configuration for a custom sub-agent with a pre-built agent instance.

    Attributes:
        name: Unique identifier for the sub-agent
        description: Description of sub-agent's purpose (shown to main agent)
        agent: Pre-configured Agent instance
    """

    name: str
    description: str
    agent: Agent  # Strands Agent instance
