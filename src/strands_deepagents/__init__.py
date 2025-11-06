"""
Strands DeepAgents - Implementation of DeepAgents pattern using Strands Agents SDK.

This package provides tools for creating "deep" agents capable of:
- Complex planning with TODO lists
- File system operations (using strands_tools)
- Sub-agent delegation
- Multi-step reasoning and execution

Adapted from the LangChain DeepAgents pattern to work with Strands Agents SDK.
"""

from strands_deepagents.factory import create_deep_agent, async_create_deep_agent
from strands_deepagents.types import SubAgent, CustomSubAgent
from strands_deepagents.state import DeepAgentState
from strands_deepagents.ai_models import get_default_model

__version__ = "0.1.0"

__all__ = [
    "create_deep_agent",
    "async_create_deep_agent",
    "SubAgent",
    "CustomSubAgent",
    "DeepAgentState",
    "get_default_model",
]
