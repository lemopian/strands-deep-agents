"""
DeepSearch Agent implementation using Strands DeepAgents.

This example demonstrates a sophisticated research agent architecture with:
- Research lead agent for strategy and coordination
- Research subagents for focused investigation
- Citations agent for adding source references
- Internet search integration (TAVILY by default)
"""

import argparse
import logging
from strands_tools import tavily
from tools import internet_search
from dotenv import load_dotenv
from prompts.research_lead import RESEARCH_LEAD_PROMPT
from prompts.research_subagent import RESEARCH_SUBAGENT_PROMPT
from prompts.citations_agent import CITATIONS_AGENT_PROMPT
from strands_deepagents import create_deep_agent, SubAgent
from strands_deepagents.ai_models import basic_claude_haiku_4_5

load_dotenv()


# Configure logging for better visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

# Configure specific loggers
logger = logging.getLogger("deepsearch")
logger.setLevel(logging.INFO)

strands_logger = logging.getLogger("strands")
strands_logger.setLevel(logging.INFO)

deepagents_logger = logging.getLogger("strands_deepagents")
deepagents_logger.setLevel(logging.DEBUG)


def create_deepsearch_agent(research_tool=tavily, tool_name: str | None = None):
    """
    Create a DeepSearch agent with research capabilities.

    Args:
        research_tool: Tool to use for research (defaults to tavily module)
        tool_name: Name of the tool to use in prompts (auto-detected if not provided)

    Returns:
        Configured DeepSearch agent
    """
    # Auto-detect tool name if not provided
    if tool_name is None:
        if hasattr(research_tool, "__name__"):
            # For functions or modules
            tool_name = research_tool.__name__
        else:
            raise ValueError(
                "Tool name not provided and could not be auto-detected, pass it as a string"
            )

    # Format prompts with the internet tool name
    lead_prompt = RESEARCH_LEAD_PROMPT.format(internet_tool_name=tool_name)
    subagent_prompt = RESEARCH_SUBAGENT_PROMPT.format(internet_tool_name=tool_name)

    # Research subagent - performs focused research tasks
    research_subagent = SubAgent(
        name="research_subagent",
        description=(
            "Specialized research agent for conducting focused investigations on specific topics. "
            "Use this agent to research specific questions, gather facts, analyze sources, and compile findings. "
            f"This agent has access to {tool_name} for comprehensive web search capabilities."
        ),
        prompt=subagent_prompt,
        tools=[research_tool],
        # model is not specified here, so it inherits the default model with interleaved thinking enabled
    )

    # Citations agent - adds source references to reports
    citations_agent = SubAgent(
        name="citations_agent",
        description=(
            "Specialized agent for adding citations to research reports. "
            "Use this agent after completing a research report to add proper source citations. "
            "Provide the report text in <synthesized_text> tags along with the source list."
        ),
        model=basic_claude_haiku_4_5(),  # No need for extended thinking nor interleaved-thinking, also, a lighter model is faster, cheaper and sufficient for this task.
        prompt=CITATIONS_AGENT_PROMPT,
        tools=[],  # No tools needed - just text processing
    )

    # Create the research lead agent
    agent = create_deep_agent(
        instructions=lead_prompt,
        subagents=[research_subagent, citations_agent],
    )

    return agent


def main():
    # pass the prompt using terminal args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default="""
    Research the current state of AI safety in 2025:

1. What are the main AI safety concerns and challenges?
2. What organizations and initiatives are leading AI safety research?
3. What recent developments or breakthroughs have occurred?
4. What regulatory frameworks are being developed?

Create a comprehensive research report with:
-- Executive summary
-- Detailed findings for each question
-- Analysis of current trends
-- Future outlook

Plan your research approach using multiple research subagents for different aspects.
""",
    )
    args = parser.parse_args()
    prompt = args.prompt

    # Create DeepSearch agent
    agent = create_deepsearch_agent(research_tool=internet_search)

    result = agent(prompt)

    logger.info("\nResearch Result:")
    logger.info(result)

    # Show the research plan
    todos = agent.state.get("todos")
    if todos:
        logger.info("\nResearch Plan Execution:")
        for todo in todos:
            status_icon = {
                "completed": "✅",
                "in_progress": "🔄",
                "pending": "⏳",
            }.get(todo["status"], "❓")
            logger.info("  %s %s", status_icon, todo["content"])
        logger.info("")

    logger.info("=" * 80)
    logger.info("DeepSearch example completed!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
