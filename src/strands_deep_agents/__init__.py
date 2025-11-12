"""
Strands DeepAgents - Implementation of DeepAgents pattern using Strands Agents SDK.

This package provides tools for creating "deep" agents capable of:
- Complex planning with TODO lists
- File system operations (using strands_tools)
- Sub-agent delegation
- Multi-step reasoning and execution
- Session persistence for state recovery

Adapted from the LangChain DeepAgents pattern to work with Strands Agents SDK.
"""

from strands_deep_agents.ai_models import get_default_model
from strands_deep_agents.factory import async_create_deep_agent, create_deep_agent
from strands_deep_agents.state import DeepAgentState, Todo, TodoStatus
from strands_deep_agents.types import CustomSubAgent, SubAgent

__version__ = "0.1.0"

__all__ = [
    "create_deep_agent",
    "async_create_deep_agent",
    "SubAgent",
    "CustomSubAgent",
    "DeepAgentState",
    "Todo",
    "TodoStatus",
    "get_default_model",
]
