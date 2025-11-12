"""
DeepSearch Prompts - Configurable research agent prompts.

This package provides prompt templates for the DeepSearch agent system:
- Research Lead: Strategic planning and coordination
- Research Subagent: Focused investigation tasks
- Citations Agent: Adding source references
"""

from .citations_agent import CITATIONS_AGENT_PROMPT
from .research_lead import RESEARCH_LEAD_PROMPT
from .research_subagent import RESEARCH_SUBAGENT_PROMPT

__all__ = [
    "RESEARCH_LEAD_PROMPT",
    "RESEARCH_SUBAGENT_PROMPT",
    "CITATIONS_AGENT_PROMPT",
]
