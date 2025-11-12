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
import os
import time

from prompts.citations_agent import CITATIONS_AGENT_PROMPT
from prompts.research_lead import RESEARCH_LEAD_PROMPT
from prompts.research_subagent import RESEARCH_SUBAGENT_PROMPT
from strands.session.file_session_manager import FileSessionManager
from strands.types.exceptions import EventLoopException
from strands_tools import file_read, file_write, tavily
from tools import internet_search
from urllib3.exceptions import ProtocolError

from strands_deep_agents import SubAgent, create_deep_agent
from strands_deep_agents.ai_models import basic_claude_haiku_4_5

# Configure logging for better visibility
# Use a file handler to avoid console output corruption during streaming
log_file = "/tmp/deepsearch.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.FileHandler(log_file, mode="w"), logging.StreamHandler()],
)

# Configure specific loggers
logger = logging.getLogger("deepsearch")
logger.setLevel(logging.INFO)

strands_logger = logging.getLogger("strands")
strands_logger.setLevel(logging.WARNING)  # Reduce noise

deepagents_logger = logging.getLogger("strands_deep_agents")
deepagents_logger.setLevel(logging.INFO)  # Reduce from DEBUG

print(f"Logging to: {log_file}")


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
            f"This agent has access to {tool_name} for comprehensive web search capabilities. "
            "Results are written to files to keep context lean."
        ),
        prompt=subagent_prompt,
        tools=[research_tool, file_write],
        model=basic_claude_haiku_4_5(),  # Use Haiku to avoid streaming corruption with large responses
    )

    # Citations agent - adds source references to reports
    citations_agent = SubAgent(
        name="citations_agent",
        description=(
            "Specialized agent for adding citations to research reports. "
            "Use this agent after completing a research report to add proper source citations. "
            "Provide the report text in <synthesized_text> tags along with the source list."
        ),
        model=basic_claude_haiku_4_5(),
        prompt=CITATIONS_AGENT_PROMPT,
        tools=[file_read, file_write],  # No tools needed - just text processing
    )
    # Disable session persistence to avoid massive context accumulation
    session_id = "example-task-session"
    storage_dir = "./.agent_sessions"
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=storage_dir,
    )

    # Create the research lead agent
    agent = create_deep_agent(
        instructions=lead_prompt
        + """

IMPORTANT CONTEXT MANAGEMENT:
- Research subagents write their findings to files (./research_findings_*.md) in the current directory to keep context lean
- When ready to synthesize, use file_read to read the research findings files from the current directory (./research_findings_*.md)
- Synthesize all findings into a comprehensive report
- Write the final report to the requested filename using file_write with current directory prefix (e.g., ./report_name.md)
- ALWAYS use the current directory prefix `./` for all file paths
- At the end, Call the citations agent to add the citations to the report.
""",
        subagents=[research_subagent, citations_agent],
        tools=[file_read, file_write],
        session_manager=session_manager,
    )

    return agent


def main():
    bypass_consent = os.environ.get("BYPASS_TOOL_CONSENT", "true")
    logger.info(f"BYPASS_TOOL_CONSENT status: {bypass_consent}")

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

Create a comprehensive research report with:
-- Executive summary
-- Detailed findings for each question

Plan your research approach using multiple research subagents for different aspects.
""",
    )
    args = parser.parse_args()
    prompt = args.prompt

    # Create DeepSearch agent
    agent = create_deepsearch_agent(research_tool=internet_search)

    # Wrap agent execution in a retry loop for ProtocolError
    max_retries = 3
    retry_delay = 5
    result = None

    for attempt in range(max_retries):
        try:
            logger.info(f"Starting agent execution (attempt {attempt + 1}/{max_retries})...")
            result = agent(prompt)
            logger.info("Agent execution completed successfully!")
            break  # Success, exit retry loop
        except (ProtocolError, EventLoopException) as e:
            # Check if it's a streaming/connection error
            error_msg = str(e).lower()
            is_retryable = any(
                keyword in error_msg
                for keyword in [
                    "response ended prematurely",
                    "protocol error",
                    "connection",
                    "timeout",
                ]
            )

            if is_retryable:
                logger.warning(
                    f"Streaming error encountered (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error("All retry attempts exhausted. Please try again later.")
                    raise
            else:
                # Non-retryable error, re-raise immediately
                logger.error(f"Non-retryable error: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error during agent execution: {e}")
            raise  # Re-raise other exceptions

    if result is None:
        logger.error("Agent execution failed after all retries")
        return

    logger.info("\nResearch completed successfully!")
    logger.info(f"Agent response: {result}")

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
