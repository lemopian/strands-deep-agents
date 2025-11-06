"""
Tests for sub-agent functionality.
"""

import pytest
from strands import tool
from strands_deepagents.sub_agents import create_sub_agent_tool, create_general_purpose_sub_agent
from strands_deepagents.types import SubAgent


class TestSubAgentCreation:
    """Test suite for sub-agent tool creation."""

    def test_create_sub_agent_tool_basic(self):
        """Test creating a basic sub-agent tool."""
        sub_agent_config = SubAgent(
            name="test_agent", description="A test agent", instructions="You are a test agent."
        )

        tool_func = create_sub_agent_tool(
            sub_agent_config=sub_agent_config,
            default_model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )

        assert tool_func.__name__ == "test_agent"
        assert "test agent" in tool_func.__doc__.lower()

    def test_sub_agent_tool_with_custom_tools(self):
        """Test sub-agent with custom tools."""

        @tool
        def custom_tool(x: str) -> str:
            """Custom tool."""
            return f"Custom: {x}"

        sub_agent_config = SubAgent(
            name="specialized_agent",
            description="Specialized agent",
            instructions="You are specialized.",
            tools=[custom_tool],
        )

        tool_func = create_sub_agent_tool(
            sub_agent_config=sub_agent_config,
            default_model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
        )

        assert tool_func.__name__ == "specialized_agent"

    def test_general_purpose_sub_agent(self):
        """Test creating the general_purpose sub-agent."""
        instructions = "You are the main agent."
        tools = []
        model_id = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

        general_agent = create_general_purpose_sub_agent(
            main_instructions=instructions, all_tools=tools, model_id=model_id
        )

        assert general_agent.name == "general_purpose"
        assert "context quarantine" in general_agent.description.lower()
        assert general_agent.instructions == instructions
        assert general_agent.tools == tools
        assert general_agent.model_id == model_id


class TestSubAgentExecution:
    """Test suite for sub-agent execution (integration tests)."""

    @pytest.mark.skip(reason="Requires actual model API access")
    def test_sub_agent_execution(self):
        """Test executing a sub-agent (requires API)."""
        # This test would require actual API credentials
        # Skipping for unit tests
        pass
