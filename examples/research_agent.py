"""
Research agent example for Strands DeepAgents.

This example demonstrates:
- Creating a research-focused deep agent
- Using external tools (http_request)
- Breaking down complex research into phases
- Documenting findings in files
"""

from strands.models import BedrockModel
from botocore.config import Config
from strands_deepagents import create_deep_agent, SubAgent
from dotenv import load_dotenv

load_dotenv()


def main():
    """Demonstrate a research agent implementation."""

    # Optional: Set environment variable to bypass tool consent
    # os.environ["BYPASS_TOOL_CONSENT"] = "true"

    print("=" * 60)
    print("Strands DeepAgents - Research Agent Example")
    print("=" * 60)
    print()

    # Import research tools from strands_tools if available
    try:
        from strands_tools import http_request, tavily

        research_tools = [tavily]
    except ImportError:
        print("Note: strands-agents-tools not installed. Some features may be limited.")
        research_tools = []

    # Create a research-focused sub-agent
    model = BedrockModel(
        model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        boto_client_config=Config(read_timeout=2400),
    )
    fact_checker = SubAgent(
        name="fact_checker",
        description="Specialized agent for verifying facts and cross-referencing information",
        prompt="""You are a fact-checking specialist. Your role is to:
        - Verify claims against multiple sources
        - Identify potential biases or inconsistencies
        - Provide confidence levels for factual statements
        - Note when information cannot be verified""",
        tools=research_tools,
        model=model,
    )

    # Create the research agent
    agent = create_deep_agent(
        instructions="""You are a research assistant specialized in thorough investigation.
        
        For research tasks:
        1. Break down the research into focused questions
        2. Investigate each question systematically
        3. Document findings in well-organized markdown files
        4. Use the fact_checker sub-agent to verify key claims
        5. Synthesize information into a cohesive report
        
        Always cite sources and maintain objectivity.""",
        tools=research_tools,
        subagents=[fact_checker],
        model=model,
    )

    # Example research task
    print("Research Task: History and Impact of DeepAgents")
    print("-" * 60)
    print()

    result = agent(
        """
    Research the concept of "DeepAgents" in AI:
    
    1. What are DeepAgents and how do they differ from simple agents?
    2. What are the key architectural components?
    3. What are practical applications and use cases?
    
    Create a comprehensive research report in 'deepagents_research.md' with:
    - An executive summary
    - Detailed findings for each question
    - Analysis of advantages and limitations
    - References and sources
    
    Plan your research approach first.
    """
    )

    print("Research Progress:")
    print(result)
    print()

    # Show the research plan
    todos = agent.state.get("todos")
    if todos:
        print("\nResearch Plan:")
        for i, todo in enumerate(todos, 1):
            status_icon = {
                "completed": "✅",
                "in_progress": "🔄",
                "pending": "⏳",
            }.get(todo["status"], "❓")
            print(f"  {status_icon} {todo['content']}")
        print()

    print("=" * 60)
    print("Research example completed!")
    print("Note: In a real scenario, this would fetch actual web data")
    print("=" * 60)


if __name__ == "__main__":
    main()
